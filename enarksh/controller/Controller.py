"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import gc
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
from enarksh.controller.event_handler.RequestNodeActionMessageEventHandler import RequestNodeActionMessageEventHandler
from enarksh.controller.event_handler.RequestPossibleNodeActionsMessageEventHandler import \
    RequestPossibleNodeActionsMessageEventHandler
from enarksh.controller.event_handler.ScheduleDefinitionMessageEventHandler import ScheduleDefinitionMessageEventHandler
from enarksh.controller.message.DynamicWorkerDefinitionMessage import DynamicWorkerDefinitionMessage
from enarksh.controller.message.JobFinishedMessage import JobFinishedMessage
from enarksh.controller.message.RequestNodeActionMessage import RequestNodeActionMessage
from enarksh.controller.message.RequestPossibleNodeActionsMessage import RequestPossibleNodeActionsMessage
from enarksh.controller.message.ScheduleDefinitionMessage import ScheduleDefinitionMessage
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

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def daemonize():
        enarksh.daemonize(os.path.join(enarksh.HOME, 'var/lock/controllerd.pid'),
                          '/dev/null',
                          os.path.join(enarksh.HOME, 'var/log/controllerd.log'),
                          os.path.join(enarksh.HOME, 'var/log/controllerd.log'))

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
        print('Start controller.')

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
    @staticmethod
    def __shutdown():
        """
        Performs the necessary actions for stopping the controller.
        """
        # Log stop of the controller.
        print('Stop controller')

    # ------------------------------------------------------------------------------------------------------------------
    def slot_schedule_termination(self, event, rst_id, _listener_data):
        """

        :param enarksh.event.Event.Event event: The event.
        :param int rst_id: The run status of the schedule.
        :param * _listener_data: Not used
        """
        del _listener_data

        schedule = event.source

        print("Schedule %s has terminated with status %s" % (schedule.sch_id, rst_id))

        self.unload_schedule(schedule.sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    def load_schedule(self, sch_id):
        """
        :param int sch_id:

        :rtype: enarksh.controller.Schedule.Schedule
        """
        print("Loading schedule '%s'." % sch_id)

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
        print("Unloading schedule '%s'." % sch_id)

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
    def _register_sockets(self):
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
    def _register_message_types(self):
        """
        Registers all message type that the controller handles at the message controller.
        """
        self.message_controller.register_message_type(DynamicWorkerDefinitionMessage.MESSAGE_TYPE)
        self.message_controller.register_message_type(JobFinishedMessage.MESSAGE_TYPE)
        self.message_controller.register_message_type(RequestNodeActionMessage.MESSAGE_TYPE)
        self.message_controller.register_message_type(RequestPossibleNodeActionsMessage.MESSAGE_TYPE)
        self.message_controller.register_message_type(ScheduleDefinitionMessage.MESSAGE_TYPE)

    # ------------------------------------------------------------------------------------------------------------------
    def _register_events_handlers(self):
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
        self.message_controller.register_listener(RequestNodeActionMessage.MESSAGE_TYPE,
                                                  RequestNodeActionMessageEventHandler.handle,
                                                  self)
        self.message_controller.register_listener(RequestPossibleNodeActionsMessage.MESSAGE_TYPE,
                                                  RequestPossibleNodeActionsMessageEventHandler.handle,
                                                  self)
        self.message_controller.register_listener(ScheduleDefinitionMessage.MESSAGE_TYPE,
                                                  ScheduleDefinitionMessageEventHandler.handle,
                                                  self)

        # Register other event handlers.
        self.event_controller.event_queue_empty.register_listener(EventQueueEmptyEventHandler.handle, self)

    # ------------------------------------------------------------------------------------------------------------------
    def main(self):
        """
        The main function of the job spawner.
        """
        self.__startup()

        self._register_sockets()

        self._register_message_types()

        self._register_events_handlers()

        self.message_controller.no_barking(5)

        self.event_controller.loop()

        self.__shutdown()

# ----------------------------------------------------------------------------------------------------------------------
