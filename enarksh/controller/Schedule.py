"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import functools
import smtplib
import sys
import traceback
from email.mime.text import MIMEText

import enarksh
from enarksh.DataLayer import DataLayer
from enarksh.controller import consumption
from enarksh.controller import resource
from enarksh.controller.node import create_node
from enarksh.event.Event import Event
from enarksh.event.EventActor import EventActor


class Schedule(EventActor):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, sch_id, host_resources):
        """
        Object constructor.

        :param int sch_id:
        :param dict host_resources:
        """
        EventActor.__init__(self)

        self._sch_id = sch_id
        """
        The ID of the schedule.

        :type: int
        """

        self._nodes = {}
        """
        A map from rnd_id to node for all the current nodes in this schedule.

        :type: dict[int,enarksh.controller.node.Node.Node]
        """

        self._children = {}
        """
        A map from rnd_id to a list with all child nodes.

        :type: dict
        """

        self._successors = {}
        """
        A map from rnd_id to a list with all (direct and indirect) successor nodes.

        :type: dict
        """

        self._schedule_load = 0
        """
        The load of this schedule. I.e. the current running (simple) nodes of this schedule.

        :type: dict
        """

        self._schedule_node = None
        """
        The node that is the actual schedule.

        :type: Node
        """

        self._activate_node = None
        """
        The node that is the activate node of the schedule.

        :type: Node
        """

        self._arrest_node = None
        """
        The node that is the arrest node of the schedule.

        :type: Node
        """

        self._mail_on_completion = True
        """
        If set a mail must be send to the operator when the schedule is finished running.

        :type: bool
        """

        self._mail_on_error = True
        """
        If set a mail must be send to the operator for each failed (simple) node.

        :type: bool
        """

        self._usr_login = ''
        """
        The user ID of the operator.

        :type: str
        """

        self._queue = set()
        """
        The queue of nodes that are ready to run.

        :type: set[enarksh.controller.node.Node.Node]
        """

        self.event_new_node_creation = Event(self)
        """
        The event that wil be fired when this schedule creates a new node.

        :type: enarksh.event.Event.Event
        """

        self.event_schedule_termination = Event(self)
        """
        The event that wil be fired when this schedule terminates.

        :type: enarksh.event.Event.Event
        """

        self._load(sch_id, host_resources)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def sch_id(self):
        """
        Returns the ID of this schedule.

        :rtype: int
        """
        return self._sch_id

    # ------------------------------------------------------------------------------------------------------------------
    def __del__(self):
        print("Deleting schedule %s" % self._sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    def _load(self, sch_id, host_resources):
        """
        Loads the schedule from the database.

        :param int sch_id:
        :param dict host_resources:
        """
        schedule = DataLayer.enk_back_schedule_get_schedule(sch_id)

        # Fetch all data of the run from the database.
        nodes_data = DataLayer.enk_back_run_get_run_nodes(schedule['run_id'])
        ports_data = DataLayer.enk_back_run_get_ports1(schedule['run_id'])
        node_ports_data = DataLayer.enk_back_run_get_ports2(schedule['run_id'])
        dependants_data = DataLayer.enk_back_run_get_dependants(schedule['srv_id'])
        consumptions_data = DataLayer.enk_back_run_get_consumptions(schedule['run_id'])
        resources_data = DataLayer.enk_back_run_get_resources(schedule['run_id'])

        # Create a lookup table for all child nodes of a node.
        tmp_child_nodes = {}
        for node_data in nodes_data.values():
            if node_data['rnd_id_parent']:
                if node_data['rnd_id_parent'] not in tmp_child_nodes:
                    tmp_child_nodes[node_data['rnd_id_parent']] = []
                tmp_child_nodes[node_data['rnd_id_parent']].append(node_data)

        # Create a lookup table for all direct successor nodes of a node.
        direct_successors = Schedule._create_successor_lookup_table1(nodes_data,
                                                                     tmp_child_nodes,
                                                                     node_ports_data,
                                                                     ports_data,
                                                                     dependants_data)

        # Create a lookup table for all direct predecessor nodes of a node.
        direct_predecessors = Schedule._create_predecessor_lookup_table1(direct_successors)

        # Create a lookup table for all (direct and indirect) successor nodes of a node.
        successors = {}
        for rnd_id_predecessor in direct_successors.keys():
            successors[rnd_id_predecessor] = {}
            for rnd_id_successor in direct_successors[rnd_id_predecessor]:
                successors[rnd_id_predecessor][rnd_id_successor] = True
                Schedule._create_successor_lookup_table3(successors[rnd_id_predecessor],
                                                         direct_successors,
                                                         rnd_id_successor)

        # Create all resources.
        resources = {}
        for node_resource_data in resources_data.values():
            for resource_data in node_resource_data:
                rsc = resource.create_resource(resource_data)
                resources[resource_data['rsc_id']] = rsc

                # Observe resource for state changes.
                rsc.event_state_change.register_listener(Schedule.slot_resource_state_change)

        # Create all consumptions.
        consumptions = {}
        for node_resource_data in consumptions_data.values():
            for consumption_data in node_resource_data:
                consumptions[consumption_data['cns_id']] = consumption.create_consumption(consumption_data,
                                                                                          host_resources,
                                                                                          resources)

        # Create all nodes.
        for node_data in nodes_data.values():
            self._nodes[node_data['rnd_id']] = create_node(node_data)

        # Initialize all nodes.
        # First initialize all simple nodes. This has the effect that signals via StateChange.notify_observer are
        # send first to (simple) successor nodes and then to parent nodes (otherwise it is possible that the schedule
        # will be set to run status ENK_RST_ID_ERROR while a simple successor node did not yet receive a signal that
        # would put this node in run status ENK_RST_ID_QUEUED.
        for node_data in nodes_data.values():
            node = self._nodes[node_data['rnd_id']]
            if node.is_simple_node():
                node.initialize(node_data,
                                schedule,
                                resources,
                                resources_data,
                                consumptions,
                                consumptions_data,
                                self._nodes,
                                tmp_child_nodes,
                                direct_predecessors,
                                direct_successors,
                                successors)

                # Observe node for state changes.
                node.event_state_change.register_listener(self.slot_node_state_change)

                # Signal a new node has been created.
                self.event_new_node_creation.fire(node)

        # Second initialize complex nodes.
        for node_data in nodes_data.values():
            node = self._nodes[node_data['rnd_id']]
            if node.is_complex_node():
                node.initialize(node_data,
                                schedule,
                                resources,
                                resources_data,
                                consumptions,
                                consumptions_data,
                                self._nodes,
                                tmp_child_nodes,
                                direct_predecessors,
                                direct_successors,
                                successors)

                # Observe node for state changes.
                node.event_state_change.register_listener(self.slot_node_state_change)

                # Signal a new node has been created.
                self.event_new_node_creation.fire(node)

        # Create a map from rnd_id to all its child nodes.
        for (rnd_id_parent, nodes) in tmp_child_nodes.items():
            self._children[rnd_id_parent] = []
            for node_data in nodes:
                self._children[rnd_id_parent].append(self._nodes[node_data['rnd_id']])

        # Create a map from rnd_id to all its successor nodes.
        for (rnd_id, edges) in successors.items():
            self._successors[rnd_id] = []
            for rnd_id_successor in edges.keys():
                self._successors[rnd_id].append(self._nodes[rnd_id_successor])

        # Store the schedule, activate, and arrest node.
        self._schedule_node = self._nodes[schedule['rnd_id_schedule']]
        self._activate_node = self._nodes[schedule['rnd_id_activate']]
        self._arrest_node = self._nodes[schedule['rnd_id_arrest']]

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _create_successor_lookup_table1(nodes_data, child_nodes_data, node_ports_data, ports_data, dependants_data):
        """
        :param dict nodes_data:
        :param dict child_nodes_data:
        :param dict node_ports_data:
        :param dict ports_data:
        :param dict dependants_data:

        :rtype: dict
        """
        direct_lookup = {}
        for node_data in nodes_data.values():
            if node_data['rnd_id'] not in child_nodes_data:
                # Node is a simple node.
                direct_lookup[node_data['rnd_id']] = []
                if node_data['rnd_id'] in node_ports_data:
                    for port in node_ports_data[node_data['rnd_id']]:
                        if port['ptt_id'] == enarksh.ENK_PTT_ID_OUTPUT:
                            if port['prt_id'] in dependants_data:
                                for edge in dependants_data[port['prt_id']]:
                                    rnd_id = ports_data[edge['prt_id_dependant']]['rnd_id']
                                    if rnd_id in child_nodes_data:
                                        # Node rnd_id is a complex node.
                                        Schedule._create_successor_lookup_table2(
                                            direct_lookup[node_data['rnd_id']],
                                            nodes_data,
                                            child_nodes_data,
                                            ports_data,
                                            dependants_data,
                                            edge['prt_id_dependant'])
                                    else:
                                        # Node rnd_id is a simple node.
                                        direct_lookup[node_data['rnd_id']].append(rnd_id)

        return direct_lookup

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _create_successor_lookup_table2(lookup, nodes_data, child_nodes_data, ports_data, dependants_data, prt_id):
        """
        :param list lookup:
        :param dict nodes_data:
        :param dict child_nodes_data:
        :param dict ports_data:
        :param dict dependants_data:
        :param prt_id:
        """
        rnd_id1 = ports_data[prt_id]['rnd_id']
        if rnd_id1 in child_nodes_data:
            # Node rnd_id is a complex node.
            if prt_id in dependants_data:
                for edge in dependants_data[prt_id]:
                    Schedule._create_successor_lookup_table2(lookup,
                                                             nodes_data,
                                                             child_nodes_data,
                                                             ports_data,
                                                             dependants_data,
                                                             edge['prt_id_dependant'])
        else:
            # Node rnd_id is a simple node.
            lookup.append(rnd_id1)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _create_successor_lookup_table3(lookup, direct_lookup, rnd_id_predecessor):
        """
        :param dict lookup:
        :param dict direct_lookup:
        :param int rnd_id_predecessor:
        """
        if rnd_id_predecessor in direct_lookup:
            for rnd_id_successor in direct_lookup[rnd_id_predecessor]:
                if rnd_id_successor not in lookup:
                    lookup[rnd_id_successor] = False
                    Schedule._create_successor_lookup_table3(lookup, direct_lookup, rnd_id_successor)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _create_predecessor_lookup_table1(direct_successors):
        """
        :param dict direct_successors:

        :rtype: dict
        """
        predecessors = {}

        for rnd_id_predecessor in direct_successors.keys():
            for rnd_id_successor in direct_successors[rnd_id_predecessor]:
                if rnd_id_successor not in predecessors:
                    predecessors[rnd_id_successor] = []
                predecessors[rnd_id_successor].append(rnd_id_predecessor)

        return predecessors

    # ------------------------------------------------------------------------------------------------------------------
    def get_all_nodes(self):
        """
        Returns all nodes in this schedule.

        :rtype: dict
        """
        return self._nodes

    # ------------------------------------------------------------------------------------------------------------------
    def get_node(self, rnd_id):
        """
        Returns a node.

        :param int rnd_id: int The ID of the requested node.

        :rtype: enarksh.controller.node.Node.Node
        """
        return self._nodes[rnd_id]

    # ------------------------------------------------------------------------------------------------------------------
    def _test_node_run_status_of_successor(self, rnd_id, statuses, seen):
        """
        :param int rnd_id:
        :param tuple statuses:
        :param seen:

        :rtype: bool
        """
        if rnd_id in self._children:
            # Node rnd_id is complex node.
            for node in self._children[rnd_id]:
                if node.rnd_id not in seen:
                    seen.add(node.rnd_id)
                    if self._test_node_run_status_of_successor(node.rnd_id, statuses, seen):
                        return True

        else:
            # Node rnd_id is a simple node.
            if self._nodes[rnd_id].rst_id in statuses:
                return True

            if rnd_id in self._successors:
                for node in self._successors[rnd_id]:
                    if node.rnd_id not in seen:
                        seen.add(node.rnd_id)
                        if node.rst_id in statuses:
                            return True

                        if self._test_node_run_status_of_successor(node.rnd_id, statuses, seen):
                            return True

        return False

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_response_template():
        actions = {enarksh.ENK_ACT_ID_TRIGGER:        {'act_id':      enarksh.ENK_ACT_ID_TRIGGER,
                                                       'act_title':   'Trigger',
                                                       'act_enabled': False},
                   enarksh.ENK_ACT_ID_RESTART:        {'act_id':      enarksh.ENK_ACT_ID_RESTART,
                                                       'act_title':   'Restart',
                                                       'act_enabled': False},
                   enarksh.ENK_ACT_ID_RESTART_FAILED: {'act_id':      enarksh.ENK_ACT_ID_RESTART_FAILED,
                                                       'act_title':   'Restart Failed',
                                                       'act_enabled': False}}

        return {'actions':            actions,
                'mail_on_completion': False,
                'mail_on_error':      False}

    # ------------------------------------------------------------------------------------------------------------------
    def request_possible_node_actions(self, rnd_id):
        """
        Returns the possible actions for a node.

        :param int rnd_id: The ID of the node.

        :rtype dict: The message with possible node actions enabled.
        """
        response = self.get_response_template()

        # Find node in map from rnd_id to node.
        node = self._nodes.get(rnd_id, None)
        if not node:
            # Node is not part of a current run of this schedule.
            return response

        # Set the mail options.
        response['mail_on_completion'] = self._mail_on_completion
        response['mail_on_error'] = self._mail_on_error

        # Get the current run status of the node.
        rst_id = node.rst_id

        if self._schedule_node.rnd_id == rnd_id:
            # Node rnd_id is the schedule it self.
            if rst_id == enarksh.ENK_RST_ID_WAITING:
                response['actions'][enarksh.ENK_ACT_ID_TRIGGER]['act_enabled'] = True
                errors = self._test_node_run_status_of_successor(rnd_id, (enarksh.ENK_RST_ID_ERROR,), set())
                if errors:
                    response['actions'][enarksh.ENK_ACT_ID_RESTART_FAILED]['act_enabled'] = True

            elif rst_id == enarksh.ENK_RST_ID_QUEUED:
                # No actions are possible.
                pass

            elif rst_id == enarksh.ENK_RST_ID_RUNNING:
                errors = self._test_node_run_status_of_successor(rnd_id, (enarksh.ENK_RST_ID_ERROR,), set())
                if errors:
                    response['actions'][enarksh.ENK_ACT_ID_RESTART_FAILED]['act_enabled'] = True

            elif rst_id == enarksh.ENK_RST_ID_COMPLETED:
                response['actions'][enarksh.ENK_ACT_ID_TRIGGER]['act_enabled'] = True

            elif rst_id == enarksh.ENK_RST_ID_ERROR:
                response['actions'][enarksh.ENK_ACT_ID_TRIGGER]['act_enabled'] = True
                response['actions'][enarksh.ENK_ACT_ID_RESTART_FAILED]['act_enabled'] = True

            else:
                raise Exception("Unexpected rst_id '%s'." % rst_id)

            return response

        if self._activate_node.rnd_id == rnd_id:
            # Node rnd_id is the trigger of the schedule.
            busy = self._test_node_run_status_of_successor(rnd_id, (enarksh.ENK_RST_ID_RUNNING,
                                                                    enarksh.ENK_RST_ID_QUEUED), set())
            if not busy:
                response['actions'][enarksh.ENK_ACT_ID_TRIGGER]['act_enabled'] = True

            return response

        if self._arrest_node.rnd_id == rnd_id:
            # No actions are possible for an arrest node of a schedule.
            return response

        # Node is not an activate node nor an arrest node of the schedule.
        if rst_id == enarksh.ENK_RST_ID_WAITING:
            # Node is waiting for 1 or more predecessors are completed.
            # No actions are possible.
            pass

        elif rst_id == enarksh.ENK_RST_ID_QUEUED:
            # All predecessor are completed, but node is waiting for resources become available.
            # No actions are possible.
            pass

        elif rst_id == enarksh.ENK_RST_ID_RUNNING:
            # Node is running.
            # No actions are possible for simple nodes.
            if node.is_complex_node():
                errors = self._test_node_run_status_of_successor(rnd_id, (enarksh.ENK_RST_ID_ERROR,), set())
                if errors:
                    response['actions'][enarksh.ENK_ACT_ID_RESTART_FAILED]['act_enabled'] = True

        elif rst_id == enarksh.ENK_RST_ID_COMPLETED:
            # Node has completed successfully.
            busy = self._test_node_run_status_of_successor(rnd_id, (enarksh.ENK_RST_ID_RUNNING,), set())
            if not busy:
                response['actions'][enarksh.ENK_ACT_ID_RESTART]['act_enabled'] = True

        elif rst_id == enarksh.ENK_RST_ID_ERROR:
            if node.is_complex_node():
                response['actions'][enarksh.ENK_ACT_ID_RESTART]['act_enabled'] = True
                response['actions'][enarksh.ENK_ACT_ID_RESTART_FAILED]['act_enabled'] = True

            elif node.is_simple_node():
                response['actions'][enarksh.ENK_ACT_ID_RESTART]['act_enabled'] = True

            else:
                raise Exception('Internal error.')

        else:
            raise Exception("Unexpected rst_id '%d'." % rst_id)

        return response

    # ------------------------------------------------------------------------------------------------------------------
    def _node_action_restart(self, rnd_id):
        """
        Restarts a node.

        :param int rnd_id: The ID of the node.

        :rtype bool: True if the controller must reload the schedule. False otherwise.
        """
        # Find node in map from rnd_id to node.
        node = self._nodes.get(rnd_id, None)
        if not node:
            # Node is not part of a current run of a this schedule.
            return False

        node.restart()

        return False

    # ------------------------------------------------------------------------------------------------------------------
    def _node_action_trigger_schedule(self, rnd_id):
        """
        Triggers the schedule.

        :param int rnd_id:

        :rtype bool: True if the controller must reload the schedule. False otherwise.
        """
        run_id = DataLayer.enk_back_schedule_trigger(self._sch_id)

        if not run_id:
            node = self._nodes[rnd_id]
            node.rst_id = enarksh.ENK_RST_ID_QUEUED

        return bool(run_id)

    # ------------------------------------------------------------------------------------------------------------------
    def _node_action_restart_failed(self, rnd_id):
        """
        Restarts a node.

        :param int rnd_id: The ID of the node.

        :rtype bool: False.
        """
        # Find node in map from rnd_id to node.
        node = self._nodes.get(rnd_id, None)
        if not node:
            # Node is not part of a current run of a this schedule.
            return False

        node.restart_failed()

        return False

    # ------------------------------------------------------------------------------------------------------------------
    def node_stop(self, rnd_id, exit_status):
        """
        :param int rnd_id:
        :param int exit_status:
        """
        # Find node in map from rnd_id to node.
        node = self._nodes.get(rnd_id, None)
        if not node:
            # Node is not part of a current run of a this schedule.
            return

        node.stop(exit_status)

    # ------------------------------------------------------------------------------------------------------------------
    def _send_mail_on_error(self, node):
        """
        Sends an email to the administrator that a simple node has failed.

        :param enarksh.controller.node.Node.Node node: The node that has failed.
        """
        if self._usr_login:
            try:
                user = DataLayer.enk_back_get_user_info(self._usr_login)

                body = "Dear Enarksh user,"
                ""
                "Job " + str(node.name) + " has run unsuccessfully."
                ""
                "Greetings from Enarksh"
                subject = "Job of schedule " + str(self._schedule_node.name) + "failed."

                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['To'] = user['usr_email']
                msg['From'] = user['usr_email']

                # Send the message via our local SMTP server.
                s = smtplib.SMTP('localhost')
                s.send_message(msg)
                s.quit()
            except Exception as exception:
                print(exception, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)

    # ------------------------------------------------------------------------------------------------------------------
    def _send_mail_on_completion(self):
        """
        Sends an email to the administrator that the schedule has completed.
        """
        if self._usr_login:
            try:
                user = DataLayer.enk_back_get_user_info(self._usr_login)

                if self._schedule_node.rst_id == enarksh.ENK_RST_ID_ERROR:
                    body = "Dear Enarksh user,"
                    ""
                    "Schedule " + str(self._schedule_node.name) + " has finished unsuccessfully."
                    ""
                    "Greetings from Enarksh"
                    subject = "Schedule " + self._schedule_node.name + "finished unsuccessfully."
                else:
                    body = "Dear Enarksh user,"
                    ""
                    "Schedule " + str(self._schedule_node.name) + " has finished successfully."
                    ""
                    "Greetings from Enarksh"
                    subject = "Schedule " + self._schedule_node.name + "finished successfully."

                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['To'] = user['usr_email']
                msg['From'] = user['usr_email']

                # Send the message via our local SMTP server.
                s = smtplib.SMTP('localhost')
                s.send_message(msg)
                s.quit()
            except Exception as exception:
                print(exception, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)

    # ------------------------------------------------------------------------------------------------------------------
    def slot_node_state_change(self, event, event_data, _listener_data):
        """
        :param enarksh.event.Event.Event event: The event.
        :param tuple[disc,disc] event_data: Tuple with the old and new state.
        :param * _listener_data: Not used.
        """
        del _listener_data

        node = event.source
        old, new = event_data

        # If required: sync the status of the node to the database.
        if old['rst_id'] != new['rst_id']:
            node.sync_state()

        # If required: update the queue.
        if old['rst_id'] != new['rst_id'] and node.is_simple_node():
            if new['rst_id'] == enarksh.ENK_RST_ID_QUEUED:
                self._queue.add(node)
            elif old['rst_id'] == enarksh.ENK_RST_ID_QUEUED:
                self._queue.discard(node)

        # Adjust the schedule load (i.e. number of running nodes) of this schedule.
        if node.is_simple_node():
            if old['rst_id'] != new['rst_id']:
                if new['rst_id'] == enarksh.ENK_RST_ID_RUNNING:
                    self._schedule_load += 1
                if old['rst_id'] == enarksh.ENK_RST_ID_RUNNING:
                    self._schedule_load -= 1

        # Adjust all mappings from rnd_id.
        if old['rnd_id'] != new['rnd_id']:
            if old['rnd_id'] in self._children:
                self._children[new['rnd_id']] = self._children[old['rnd_id']]
                del self._children[old['rnd_id']]

            self._nodes[new['rnd_id']] = self._nodes[old['rnd_id']]
            del self._nodes[old['rnd_id']]

            if old['rnd_id'] in self._successors:
                self._successors[new['rnd_id']] = self._successors[old['rnd_id']]
                del self._successors[old['rnd_id']]

        # If a simple node has failed send mail to administrator.
        if node.is_simple_node() and old['rst_id'] != new['rst_id']:
            if new['rst_id'] == enarksh.ENK_RST_ID_ERROR and self._mail_on_error:
                self._send_mail_on_error(node)

        # If the schedule has finished send an mail to the administrator.
        if node == self._schedule_node and old['rst_id'] != new['rst_id']:
            if new['rst_id'] in (enarksh.ENK_RST_ID_ERROR, enarksh.ENK_RST_ID_COMPLETED):
                self._send_mail_on_completion()

        # If the schedule has terminated inform all observer of this event.
        if node == self._schedule_node and old['rst_id'] != new['rst_id']:
            if new['rst_id'] in (enarksh.ENK_RST_ID_ERROR, enarksh.ENK_RST_ID_COMPLETED):
                self.event_schedule_termination.fire(new['rst_id'])

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def slot_resource_state_change(event, _event_data, _listener_data):
        """
        :param enarksh.event.Event.Event event: The event.
        :param * _event_data: Not used.
        :param * _listener_data: Not used.
        """
        del _event_data, _listener_data

        rsc = event.source
        rsc.sync_state()

    # ------------------------------------------------------------------------------------------------------------------
    def get_schedule_load(self):
        """
        Returns the schedule load of this schedule. I.e. the number of nodes of ths schedule that are currently running.

        :rtype: int
        """
        return self._schedule_load

    # ------------------------------------------------------------------------------------------------------------------
    def get_activate_node(self):
        """
        Returns the node that is the activate node of this schedule.

        :rtype: enarksh.controller.node.Node
        """
        return self._activate_node

    # ------------------------------------------------------------------------------------------------------------------
    def request_node_action(self, rnd_id, act_id, usr_login, mail_on_completion, mail_on_error):
        """
        Executes a node action.

        :param int rnd_id: The ID of the node.
        :param int act_id: The ID of the requested action.
        :param str usr_login: The name of the user who has requested the node action.
        :param bool mail_on_completion: If True the user wants to receive a mail when the schedule has completed.
        :param bool mail_on_error: If True the user wants to receive a mail when an error occurs.

        :rtype bool: True if the controller must reload the schedule. False otherwise.
        """
        # Store the mail options.
        self._usr_login = usr_login
        self._mail_on_completion = mail_on_completion
        self._mail_on_error = mail_on_error

        if self._schedule_node.rnd_id == rnd_id:
            # Node is the schedule is self.
            if act_id == enarksh.ENK_ACT_ID_TRIGGER:
                return self._node_action_trigger_schedule(rnd_id)

            if act_id == enarksh.ENK_ACT_ID_RESTART_FAILED:
                return self._node_action_restart_failed(rnd_id)

            raise RuntimeError("Unknown or unsupported act_id '%s'." % act_id)

        if self._activate_node.rnd_id == rnd_id:
            # Node is the activate node of the schedule.
            if act_id == enarksh.ENK_ACT_ID_TRIGGER:
                return self._node_action_trigger_schedule(rnd_id)

            raise RuntimeError("Unknown or unsupported act_id '%s'." % act_id)

        if self._arrest_node.rnd_id == rnd_id:
            # Node is the arrest node of the schedule. No actions are possible.
            raise RuntimeError("Unknown or unsupported act_id '%s'." % act_id)

        # Node is a "normal" node in the schedule.
        if act_id == enarksh.ENK_ACT_ID_RESTART:
            return self._node_action_restart(rnd_id)

        if act_id == enarksh.ENK_ACT_ID_RESTART_FAILED:
            return self._node_action_restart_failed(rnd_id)

        raise RuntimeError("Unknown or unsupported act_id '%s'." % act_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def queue_compare(node1, node2):
        """
        Compares two nodes for sorting queued nodes.

        :param enarksh.controller.node.Node node1:
        :param enarksh.controller.node.Node node2:

        :rtype: int
        """
        # Sort by scheduling weight.
        cmp = node2.scheduling_weight - node1.scheduling_weight

        if cmp == 0:
            if node1.name.lower() < node2.name.lower():
                cmp = -1
            elif node1.name.lower() > node2.name.lower():
                cmp = 1
            else:
                cmp = 0

        return cmp

    # ------------------------------------------------------------------------------------------------------------------
    def get_queue(self):
        """
        Returns the queued nodes sorted by scheduling wait.

        :rtype: list[enarksh.controller.node.Node.Node]
        """
        return sorted(self._queue, key=functools.cmp_to_key(Schedule.queue_compare))

# ----------------------------------------------------------------------------------------------------------------------
