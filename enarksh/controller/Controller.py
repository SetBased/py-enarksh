"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import functools
import gc
import os
import pwd
import sys
import traceback

import zmq

import enarksh
from enarksh.DataLayer import DataLayer
from enarksh.controller import resource
from enarksh.controller.Schedule import Schedule
from enarksh.xml_reader.XmlReader import XmlReader
from enarksh.xml_reader.node.FakeParent import FakeParent


class Controller:
    _instance = None

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        Controller._instance = self

        self._zmq_context = None
        """
        :type: zmq.Context
        """

        self._zmq_pull_socket = zmq.sugar.socket.Socket
        """
        :type: zmq.sugar.socket.Socket
        """

        self._zmq_lockstep_socket = None
        """
        :type: zmq.sugar.socket.Socket
        """

        self._zmq_spanner = None
        """
        :type: Socket
        """

        self._zmq_logger = None
        """
        :type: Socket
        """

        self._host_resources = {}
        """
        All resources defined at host level.

        :type: dict
        """

        self._schedules = {}
        """
        All the current schedules.

        :type: dict
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _zmq_init(self):
        self._zmq_context = zmq.Context()

        # Create socket for asynchronous incoming messages.
        self._zmq_pull_socket = self._zmq_context.socket(zmq.PULL)
        self._zmq_pull_socket.bind(enarksh.CONTROLLER_PULL_END_POINT)

        # Create socket for lockstep incoming messages.
        self._zmq_lockstep_socket = self._zmq_context.socket(zmq.REP)
        self._zmq_lockstep_socket.bind(enarksh.CONTROLLER_LOCKSTEP_END_POINT)

        # Create socket for sending asynchronous messages to the spanner.
        self._zmq_spanner = self._zmq_context.socket(zmq.PUSH)
        self._zmq_spanner.connect(enarksh.SPAWNER_PULL_END_POINT)

        # Create socket for sending asynchronous messages to the logger.
        self._zmq_logger = self._zmq_context.socket(zmq.PUSH)
        self._zmq_logger.connect(enarksh.LOGGER_PULL_END_POINT)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def daemonize():
        enarksh.daemonize(os.path.join(enarksh.HOME, 'var/lock/controllerd.pid'),
                          '/dev/null',
                          os.path.join(enarksh.HOME, 'var/log/controllerd.log'),
                          os.path.join(enarksh.HOME, 'var/log/controllerd.log'))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _set_unprivileged_user():
        """
        Set the real and effective user and group to an unprivileged user.
        """
        _, _, uid, gid, _, _, _ = pwd.getpwnam('enarksh')

        os.setresgid(gid, gid, 0)
        os.setresuid(uid, uid, 0)

    # ------------------------------------------------------------------------------------------------------------------
    def _create_host_resources(self):
        """
        Creates resources defined at host level.
        """
        resources_data = DataLayer.enk_back_get_host_resources()
        for resource_data in resources_data:
            self._host_resources[resource_data['rsc_id']] = resource.create_resource(resource_data)

    # ------------------------------------------------------------------------------------------------------------------
    def _startup(self):
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

        # Sanitise the data in the database.
        DataLayer.enk_back_controller_init()

        # Create resources defined at host level.
        self._create_host_resources()

        # Set the effective user and group to an unprivileged user and group.
        # self._set_unprivileged_user()

        # Become a daemon.
        # self.__daemonize()

        self._zmq_init()

        # Housekeeping to track statuses of nodes.
        Schedule.register_observer_schedule_termination(self.slot_schedule_termination)

        # Commit transaction and close connection to MySQL.
        DataLayer.commit()
        DataLayer.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def slot_schedule_termination(self, schedule, rst_id):
        """
        :param enarksh.controller.Schedule.Schedule schedule: The schedule.
        :param int rst_id:
        """
        print("Schedule %s has terminated with status %s" % (schedule.sch_id, rst_id))

        self._unload_schedule(schedule.sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    def _load_schedule(self, sch_id):
        """
        :param int sch_id:

        :rtype: enarksh.controller.Schedule.Schedule
        """
        print("Loading schedule '%s'." % sch_id)

        # Load the schedule.
        schedule = Schedule(sch_id, self._host_resources)

        # Register the schedule.
        self._schedules[sch_id] = schedule

        return schedule

    # ------------------------------------------------------------------------------------------------------------------
    def _unload_schedule(self, sch_id):
        """
        :param int sch_id:
        """
        print("Unloading schedule '%s'." % sch_id)

        if sch_id in self._schedules:
            schedule = self._schedules[sch_id]

            # Remove the schedule.
            del self._schedules[sch_id]

            schedule.destroy()

            gc.collect()

    # ------------------------------------------------------------------------------------------------------------------
    def _reload_schedule(self, sch_id):
        """
        :param int sch_id:

        :rtype: enarksh.controller.Schedule.Schedule
        """
        self._unload_schedule(sch_id)

        return self._load_schedule(sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def queue_compare(schedule1, schedule2):
        """
        Compares two schedules for sorting queued nodes.

        :param enarksh.controller.Schedule.Schedule schedule1:
        :param enarksh.controller.Schedule.Schedule schedule2:

        :rtype:
        """
        return -(schedule1.get_schedule_load() - schedule2.get_schedule_load)

    # ------------------------------------------------------------------------------------------------------------------
    def _queue_handler(self):
        """
        Starts node that are queued and for which there are enough resources available.
        """
        # Return immediately if there are no loaded schedules.
        if not self._schedules:
            return

        DataLayer.connect()
        DataLayer.start_transaction()

        while True:
            start = False
            if self._schedules:
                schedules = sorted(self._schedules, key=functools.cmp_to_key(Controller.queue_compare))
                schedule = self._schedules[schedules[0]]
                queue = schedule.get_queue()
                for node in queue:
                    # Inquire if there are enough resources available for the node.
                    start = node.inquire_resources()
                    if start:
                        span_job = node.start()

                        # If required send a message to the spanner.
                        if span_job:
                            message = node.get_start_message(schedule.sch_id)
                            self._zmq_spanner.send_pyobj(message)

                        else:
                            node.stop(0)

                        # If a node has been started leave inner loop.
                        break

            # If no node has been started leave the outer loop.
            if not start:
                break

        # Commit the last transaction (if any) and close the connection to the database.
        DataLayer.commit()
        DataLayer.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def _get_schedule_by_sch_id(self, sch_id):
        """
        Returns a schedule.

        :param int sch_id: The ID of the schedule.

        :rtype: enarksh.controller.Schedule.Schedule
        """
        schedule = self._schedules.get(int(sch_id), None)
        if not schedule:
            # Load the schedule if the schedule is not currently loaded.
            schedule = self._load_schedule(sch_id)

        return schedule

    # ------------------------------------------------------------------------------------------------------------------
    def _get_possible_node_actions(self, sch_id, rnd_id):
        """
        Returns the possible actions for a node.

        :param int sch_id: The ID of the schedule of the node.
        :param int rnd_id: The ID of the node.

        :rtype dict[str, bool|dict[int, dict[str, mixed]]]: Dictionary with possible node actions.
        """
        message = {'actions':            {enarksh.ENK_ACT_ID_TRIGGER:        {'act_id':      enarksh.ENK_ACT_ID_TRIGGER,
                                                                              'act_title':   'Trigger',
                                                                              'act_enabled': False},
                                          enarksh.ENK_ACT_ID_RESTART:        {'act_id':      enarksh.ENK_ACT_ID_RESTART,
                                                                              'act_title':   'Restart',
                                                                              'act_enabled': False},
                                          enarksh.ENK_ACT_ID_RESTART_FAILED: {
                                              'act_id':      enarksh.ENK_ACT_ID_RESTART_FAILED,
                                              'act_title':   'Restart Failed',
                                              'act_enabled': False}},
                   'mail_on_completion': False,
                   'mail_on_error':      False}

        # Find the schedule of the node.
        schedule = self._get_schedule_by_sch_id(sch_id)
        if not schedule:
            # Node rnd_id is not part of a current run of a current schedule revision.
            return message

        return schedule.request_possible_node_actions(rnd_id, message)

    # ------------------------------------------------------------------------------------------------------------------
    def _message_handler_request_possible_node_actions(self, message):
        """
        Handles a request (from the web interface) for possible actions of a certain node.

        :param dict message: The message of the request.
        """
        sch_id = int(message['sch_id'])
        rnd_id = int(message['rnd_id'])

        response = self._get_possible_node_actions(sch_id, rnd_id)

        # Send the message to the web interface.
        self._zmq_lockstep_socket.send_json(response)

    # ------------------------------------------------------------------------------------------------------------------
    def _message_handler_schedule_definition(self, message):
        """
        Handles a request (from the operator) for loading a new schedule.

        :param dict message: The message of the request.
        """
        try:
            # Validate XML against XSD.
            reader = XmlReader()
            schedule = reader.parse_schedule(message['xml'], message['filename'])

            # Test schedule is currently running.
            name = schedule.name
            if name in self._schedules:
                raise Exception("Schedule '%s' is currently running." % name)

            # Insert the XML definition as BLOB in tot the database.
            blb_id = DataLayer.enk_blob_insert_blob(os.path.basename(message['filename']), 'text/xml', message['xml'])
            srv_id = DataLayer.enk_reader_schedule_create_revision(blb_id, name)
            if not srv_id:
                raise Exception("Schedule '%s' is already loaded." % name)

            # Store the new schedule definition into the database.
            schedule.store(srv_id, 1)
            DataLayer.enk_back_schedule_revision_create_run(srv_id)

            response = {'ret':     0,
                        'message': "Schedule '%s' successfully loaded." % name}
        except Exception as exception:
            print(exception, file=sys.stderr)
            response = {'ret':     -1,
                        'message': str(exception)}
            traceback.print_exc(file=sys.stderr)

        self._zmq_lockstep_socket.send_json(response)

    # ------------------------------------------------------------------------------------------------------------------
    def _message_handler_dynamic_worker_definition(self, message):
        """
        Handles a request for loading a dynamic worker definition.

        :param dict message: The message of the request.
        """
        try:
            sch_id = int(message['sch_id'])
            rnd_id = int(message['rnd_id'])

            print('rnd_id: ' + str(rnd_id))

            # Get info of the dynamic node.
            info = DataLayer.enk_back_run_node_get_dynamic_info_by_generator(rnd_id)

            schedule = self._get_schedule_by_sch_id(sch_id)
            parent = FakeParent(schedule,
                                self._host_resources,
                                info['nod_id_outer_worker'],
                                info['rnd_id_outer_worker'])

            # Validate XML against XSD.
            reader = XmlReader()
            inner_worker = reader.parse_dynamic_worker(message['definition'], parent)
            name = inner_worker.name

            # Note: Dynamic node is the parent of the worker node which is the parent of the inner worker node.
            inner_worker.set_levels(info['nod_recursion_level'] + 2)

            # Store the dynamically defined inner worker node.
            inner_worker.store(info['srv_id'], 0)

            # Create dependencies between the input and output port of the worker node and its child node(s).
            DataLayer.enk_back_node_dynamic_add_dependencies(info['nod_id_outer_worker'], inner_worker.nod_id)

            # XXX trigger reload of front end

            # Unload the schedule to force a reload of the schedule with new nodes added.
            self._unload_schedule(sch_id)

            response = {'ret':     0,
                        'message': "Worker '%s' successfully loaded." % name}

        except Exception as exception:
            print(exception, file=sys.stderr)
            response = {'ret':     -1,
                        'message': str(exception)}
            traceback.print_exc(file=sys.stderr)

        self._zmq_lockstep_socket.send_json(response)

    # ------------------------------------------------------------------------------------------------------------------
    def _message_handler_request_node_action(self, message):
        """
        Executes a node action request.

        :param dict message: dict The message of the request.
        """
        # Compose a response message for the web interface.
        response = {'ret':     0,
                    'new_run': 0,
                    'message': 'OK'}

        try:
            sch_id = int(message['sch_id'])
            rnd_id = int(message['rnd_id'])
            act_id = int(message['act_id'])

            actions = self._get_possible_node_actions(sch_id, rnd_id)
            if act_id not in actions['actions'] or not actions['actions'][act_id]['act_enabled']:
                response['ret'] = -1
                response['message'] = 'Not a valid action'
            else:
                schedule = self._get_schedule_by_sch_id(sch_id)
                reload = schedule.request_node_action(rnd_id,
                                                      act_id,
                                                      message['usr_login'],
                                                      (message['mail_on_completion']),
                                                      (message['mail_on_error']))
                if reload:
                    # Schedule must be reloaded.
                    schedule = self._reload_schedule(schedule.sch_id)
                    # A reload is only required when the schedule is been triggered. However, this trigger is lost by
                    # reloading the schedule. So, resend the trigger.
                    schedule.request_node_action(schedule.get_activate_node().rnd_id,
                                                 act_id,
                                                 message['usr_login'],
                                                 (message['mail_on_completion']),
                                                 (message['mail_on_error']))

                    if act_id == enarksh.ENK_ACT_ID_TRIGGER:
                        response['new_run'] = 1

        except Exception as exception:
            print(exception, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

            response['ret'] = -1
            response['message'] = 'Internal error'

        # Send the message to the web interface.
        self._zmq_lockstep_socket.send_json(response)

    # ------------------------------------------------------------------------------------------------------------------
    def _message_handler_node_stop(self, message):
        """
        Handles a message sent by the spanner after a job has finished.

        :param dict message:
        """
        schedule = self._get_schedule_by_sch_id(message['sch_id'])
        schedule.event_node_stop(message['rnd_id'], message['exit_status'])

    # ------------------------------------------------------------------------------------------------------------------
    def _message_handler(self):
        """
        Waits for a new messages and processes these messages.
        """
        poller = zmq.Poller()
        poller.register(self._zmq_pull_socket, zmq.POLLIN)
        poller.register(self._zmq_lockstep_socket, zmq.POLLIN)

        socks = dict(poller.poll())

        DataLayer.connect()
        DataLayer.start_transaction()

        if self._zmq_pull_socket in socks:
            message = self._zmq_pull_socket.recv_pyobj()

            # if message['type'] == 'node_stop':
            self._message_handler_node_stop({'sch_id':      message.sch_id,
                                             'rnd_id':      message.rnd_id,
                                             'exit_status': message.exit_status})

            # else:
            #    raise Exception("Unknown message type '%s'." % message['type'])

        if self._zmq_lockstep_socket in socks:
            message = self._zmq_lockstep_socket.recv_json()

            if message['type'] == 'schedule_definition':
                self._message_handler_schedule_definition(message)

            elif message['type'] == 'request_node_action':
                self._message_handler_request_node_action(message)

            elif message['type'] == 'request_possible_node_actions':
                self._message_handler_request_possible_node_actions(message)

            elif message['type'] == 'dynamic_worker_definition':
                self._message_handler_dynamic_worker_definition(message)

            else:
                raise Exception("Unknown message type '%s'." % message['type'])

        DataLayer.commit()
        DataLayer.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def main(self):
        """
        The main function of the job controller.
        """
        # Perform the necessary actions for starting the controller.
        self._startup()

        while True:
            try:
                # Wait for new messages and process these messages.
                self._message_handler()

                # Try to start nodes that are queued.
                self._queue_handler()

            except Exception as exception1:
                try:
                    DataLayer.rollback()
                    DataLayer.disconnect()
                except Exception as exception2:
                    print(exception2, file=sys.stderr)
                    traceback.print_exc(file=sys.stderr)
                print(exception1, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)

# ----------------------------------------------------------------------------------------------------------------------
