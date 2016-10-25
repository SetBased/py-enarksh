"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import gc
import logging
import os
import pwd

import zmq

import enarksh
from enarksh.DataLayer import DataLayer
from enarksh.controller import resource
from enarksh.controller.Schedule import Schedule
from enarksh.controller.event_handler.DynamicWorkerDefinitionMessageEventHandler import \
    DynamicWorkerDefinitionMessageEventHandler
from enarksh.controller.event_handler.EventQueueEmptyEventHandler import EventQueueEmptyEventHandler
from enarksh.controller.event_handler.JobFinishedMessageEventHandler import JobFinishedMessageEventHandler
from enarksh.controller.event_handler.MailOperatorEventHandler import MailOperatorEventHandler
from enarksh.controller.event_handler.NagiosMessageEventHandler import NagiosMessageEventHandler
from enarksh.controller.event_handler.NodeActionMessageEventHandler import NodeActionMessageEventHandler
from enarksh.controller.event_handler.NodeActionMessageWebEventHandler import NodeActionMessageWebEventHandler
from enarksh.controller.event_handler.PossibleNodeActionsWebMessageEventHandler import \
    PossibleNodeActionsWebMessageEventHandler
from enarksh.controller.event_handler.ScheduleDefinitionMessageEventHandler import ScheduleDefinitionMessageEventHandler
from enarksh.controller.message.DynamicWorkerDefinitionMessage import DynamicWorkerDefinitionMessage
from enarksh.controller.message.JobFinishedMessage import JobFinishedMessage
from enarksh.controller.message.NagiosMessage import NagiosMessage
from enarksh.controller.message.NodeActionMessage import NodeActionMessage
from enarksh.controller.message.NodeActionWebMessage import NodeActionWebMessage
from enarksh.controller.message.PossibleNodeActionsWebMessage import PossibleNodeActionsWebMessage
from enarksh.controller.message.ScheduleDefinitionMessage import ScheduleDefinitionMessage
from enarksh.controller.node import Node
from enarksh.event.Event import Event
from enarksh.event.EventActor import EventActor
from enarksh.event.EventController import EventController
from enarksh.message.MessageController import MessageController


class Controller(EventActor):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        self.event_controller = EventController()
        """
        The event controller.

        :type: enarksh.event.EventController.EventController
        """

        EventActor.__init__(self)

        self.message_controller = MessageController()
        """
        The message controller.

        :type: enarksh.message.MessageController.MessageController
        """

        self.host_resources = {}
        """
        All resources defined at host level.

        :type: dict
        """

        self.schedules = {}
        """
        All the current schedules.

        :type: dict[int,enarksh.controller.Schedule.Schedule]
        """

        self.__log = logging.getLogger('enarksh')
        """
        The logger.

        :type: logging.Logger
        """

        # Create event for a new node has been created.
        Node.event_new_node_creation = Event(self)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __set_unprivileged_user():
        """
        Set the real and effective user and group to an unprivileged user.
        """
        _, _, uid, gid, _, _, _ = pwd.getpwnam('enarksh')

        os.setresgid(gid, gid, 0)
        os.setresuid(uid, uid, 0)

    # ------------------------------------------------------------------------------------------------------------------
    def __create_host_resources(self):
        """
        Creates resources defined at host level.
        """
        resources_data = DataLayer.enk_back_get_host_resources()
        for resource_data in resources_data:
            self.host_resources[resource_data['rsc_id']] = resource.create_resource(resource_data)

    # ------------------------------------------------------------------------------------------------------------------
    def __startup(self):
        """
        Performs the necessary actions for starting the controller daemon.
        """
        self.__log.info('Starting controller')

        # Set database configuration options.
        DataLayer.config['host'] = enarksh.MYSQL_HOSTNAME
        DataLayer.config['user'] = enarksh.MYSQL_USERNAME
        DataLayer.config['password'] = enarksh.MYSQL_PASSWORD
        DataLayer.config['database'] = enarksh.MYSQL_SCHEMA
        DataLayer.config['port'] = enarksh.MYSQL_PORT
        DataLayer.config['autocommit'] = False

        # Connect to the MySQL.
        DataLayer.connect()
        DataLayer.start_transaction()

        # Sanitise the data in the database.
        DataLayer.enk_back_controller_init()

        # Create resources defined at host level.
        self.__create_host_resources()

        # Set the effective user and group to an unprivileged user and group.
        self.__set_unprivileged_user()

        # Commit transaction and close connection to MySQL.
        DataLayer.commit()

    # ------------------------------------------------------------------------------------------------------------------
    def __shutdown(self):
        """
        Performs the necessary actions for stopping the controller.
        """
        self.__log.info('Stopping controller')

    # ------------------------------------------------------------------------------------------------------------------
    def slot_schedule_termination(self, event, rst_id, _listener_data):
        """

        :param enarksh.event.Event.Event event: The event.
        :param int rst_id: The run status of the schedule.
        :param * _listener_data: Not used
        """
        del _listener_data

        schedule = event.source

        self.__log.info('Schedule {} has terminated with status {}'.format(schedule.sch_id, rst_id))

        self.unload_schedule(schedule.sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    def load_schedule(self, sch_id):
        """
        :param int sch_id:

        :rtype: enarksh.controller.Schedule.Schedule
        """
        self.__log.info('Loading schedule {}'.format(sch_id))

        # Load the schedule.
        schedule = Schedule(sch_id, self.host_resources)
        schedule.event_schedule_termination.register_listener(self.slot_schedule_termination)

        # Register the schedule.
        self.schedules[sch_id] = schedule

        return schedule

    # ------------------------------------------------------------------------------------------------------------------
    def unload_schedule(self, sch_id):
        """
        :param int sch_id:
        """
        self.__log.info('Unloading schedule {}'.format(sch_id))

        if sch_id in self.schedules:
            # Remove the schedule.
            del self.schedules[sch_id]

            gc.collect()

    # ------------------------------------------------------------------------------------------------------------------
    def reload_schedule(self, sch_id):
        """
        :param int sch_id:

        :rtype: enarksh.controller.Schedule.Schedule
        """
        self.unload_schedule(sch_id)

        return self.load_schedule(sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    def get_schedule_by_sch_id(self, sch_id):
        """
        Returns a schedule.

        :param int sch_id: The ID of the schedule.

        :rtype: enarksh.controller.Schedule.Schedule
        """
        schedule = self.schedules.get(int(sch_id), None)
        if not schedule:
            # Load the schedule if the schedule is not currently loaded.
            schedule = self.load_schedule(sch_id)

        return schedule

    # ------------------------------------------------------------------------------------------------------------------
    def __register_sockets(self):
        """
        Registers ZMQ sockets for communication with other processes in Enarksh.
        """
        # Register socket for receiving asynchronous incoming messages.
        self.message_controller.register_end_point('pull', zmq.PULL, enarksh.CONTROLLER_PULL_END_POINT)

        # Create socket for lockstep incoming messages.       .
        self.message_controller.register_end_point('lockstep', zmq.REP, enarksh.CONTROLLER_LOCKSTEP_END_POINT)

        # Create socket for sending asynchronous messages to the spanner.
        self.message_controller.register_end_point('spawner', zmq.PUSH, enarksh.SPAWNER_PULL_END_POINT)

        # Create socket for sending asynchronous messages to the logger.
        self.message_controller.register_end_point('logger', zmq.PUSH, enarksh.LOGGER_PULL_END_POINT)

    # ------------------------------------------------------------------------------------------------------------------
    def __register_message_types(self):
        """
        Registers all message type that the controller handles at the message controller.
        """
        self.message_controller.register_message_type(DynamicWorkerDefinitionMessage.MESSAGE_TYPE)
        self.message_controller.register_message_type(JobFinishedMessage.MESSAGE_TYPE)
        self.message_controller.register_message_type(NagiosMessage.MESSAGE_TYPE)
        self.message_controller.register_message_type(NodeActionMessage.MESSAGE_TYPE)
        self.message_controller.register_message_type(ScheduleDefinitionMessage.MESSAGE_TYPE)
        self.message_controller.register_message_type(NodeActionWebMessage.MESSAGE_TYPE)
        self.message_controller.register_message_type(PossibleNodeActionsWebMessage.MESSAGE_TYPE)

        # Register JSON messages.
        self.message_controller.register_json_message_creator(PossibleNodeActionsWebMessage.MESSAGE_TYPE,
                                                              PossibleNodeActionsWebMessage.create_from_json)
        self.message_controller.register_json_message_creator(NodeActionWebMessage.MESSAGE_TYPE,
                                                              NodeActionWebMessage.create_from_json)

    # ------------------------------------------------------------------------------------------------------------------
    def __register_events_handlers(self):
        """
        Registers all event handlers at the event controller.
        """
        # Register message received event handlers.
        self.message_controller.register_listener(DynamicWorkerDefinitionMessage.MESSAGE_TYPE,
                                                  DynamicWorkerDefinitionMessageEventHandler.handle,
                                                  self)
        self.message_controller.register_listener(JobFinishedMessage.MESSAGE_TYPE,
                                                  JobFinishedMessageEventHandler.handle,
                                                  self)
        self.message_controller.register_listener(NagiosMessage.MESSAGE_TYPE,
                                                  NagiosMessageEventHandler.handle,
                                                  self)
        self.message_controller.register_listener(NodeActionMessage.MESSAGE_TYPE,
                                                  NodeActionMessageEventHandler.handle,
                                                  self)
        self.message_controller.register_listener(ScheduleDefinitionMessage.MESSAGE_TYPE,
                                                  ScheduleDefinitionMessageEventHandler.handle,
                                                  self)
        self.message_controller.register_listener(NodeActionWebMessage.MESSAGE_TYPE,
                                                  NodeActionMessageWebEventHandler.handle,
                                                  self)
        self.message_controller.register_listener(PossibleNodeActionsWebMessage.MESSAGE_TYPE,
                                                  PossibleNodeActionsWebMessageEventHandler.handle,
                                                  self)

        # Register other event handlers.
        self.event_controller.event_queue_empty.register_listener(EventQueueEmptyEventHandler.handle, self)

        Node.event_new_node_creation.register_listener(MailOperatorEventHandler.handle_node_creation)

    # ------------------------------------------------------------------------------------------------------------------
    def main(self):
        """
        The main function of the job spawner.
        """
        self.__startup()

        self.__register_sockets()

        self.__register_message_types()

        self.__register_events_handlers()

        self.message_controller.no_barking(5)

        self.event_controller.loop()

        self.__shutdown()

# ----------------------------------------------------------------------------------------------------------------------
