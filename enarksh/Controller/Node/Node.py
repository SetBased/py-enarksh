"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc
from time import strftime, gmtime

import enarksh
from enarksh.DataLayer import DataLayer
from enarksh.Controller.StateChange import StateChange


class Node(StateChange):
    """
    Abstract class for objects in the controller of type 'Node'.
    """
    _rst_id_weight = {enarksh.ENK_RST_ID_RUNNING: 5,
                      enarksh.ENK_RST_ID_QUEUED: 4,
                      enarksh.ENK_RST_ID_ERROR: 3,
                      enarksh.ENK_RST_ID_WAITING: 2,
                      enarksh.ENK_RST_ID_COMPLETED: 1}

    _weight_rst_id = {5: enarksh.ENK_RST_ID_RUNNING,
                      4: enarksh.ENK_RST_ID_QUEUED,
                      3: enarksh.ENK_RST_ID_ERROR,
                      2: enarksh.ENK_RST_ID_WAITING,
                      1: enarksh.ENK_RST_ID_COMPLETED}

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node_data):
        """
        Object constructor

        :param dict node_data:
        """
        StateChange.__init__(self)

        self._rnd_id = node_data['rnd_id']
        """
        The ID of this (run) node.

        :type:
        """

        self._node_name = str(node_data['nod_name'], 'utf-8')  # @todo XXX DataLayer encoding issue
        """
        The name of this node.

        :type: str
        """

        self._rst_id = node_data['rst_id']
        """
        The ID of the run status of this node.

        :type:
        """

        self._rnd_datetime_start = node_data['rnd_datetime_start']
        """
        The epoch this node has been started.

        :type:
        """

        self._rnd_datetime_stop = node_data['rnd_datetime_stop']
        """
        The epoch this node has finished.

        :type:
        """

        self._exit_status = None
        """
        The exit status of the job of this node.

        :type: bool
        """

        self.consumptions = []
        """
        The consumptions of this node.

        :type: list
        """

        self.resources = []
        """
        The resources of this node.

        :type: list
        """

        self._scheduling_weight = 0
        """
        The weight of this node to be taken into account when sorting queued nodes.

        :type: int
        """

        self._parent_node = None
        """
        The parent node of this node.

        :type: None|enarksh.Controller.Node.Node.Node
        """

        self._child_nodes = []
        """
        The child nodes of this node. This list is empty for simple nodes.

        :type: list
        """

        self._predecessor_nodes = []
        """
        The direct (simple) predecessor nodes of this node. This list is empty for complex nodes.

        :type: list
        """

        self._successor_nodes = []
        """
        The direct (simple) successor nodes of this node. This list is empty for complex nodes.

        :type: list
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def name(self):
        """
        Getter for name. Returns the name of this node.

        :rtype: str
        """
        return self._node_name

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def rnd_id(self):
        """
        Getter for rnd_id. Returns the ID of this node.

        :rtype: int
        """
        return self._rnd_id

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def rst_id(self):
        """
        Getter for rst_id. Returns the ID of the run status of this node.

        :rtype: int
        """
        return self._rst_id

    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    @rst_id.setter
    def rst_id(self, rst_id):
        """
        Setter for rst_id. Sets the the run status of this node.

        :param int rst_id: The ID of the run status.
        """
        self.rst_id = rst_id

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def schedule_wait(self):
        """
        Return the scheduling wait (i.e. the number (direct and indirect) of simple successors).

        :rtype: int
        """
        return self._scheduling_weight

    # ------------------------------------------------------------------------------------------------------------------
    def get_state_attributes(self):
        """
        :rtype: dict[str,int]
        """
        return {'rnd_id': self.rnd_id,
                'rst_id': self.rst_id}

    # ------------------------------------------------------------------------------------------------------------------
    def __del__(self):
        # print("Deleting node %s" % self.rnd_id)
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def destroy(self):
        StateChange.unregister_all_observers(self)
        self.resources = []
        self.consumptions = []
        self._child_nodes = []
        self._parent_node = None
        self._predecessor_nodes = []
        self._successor_nodes = []

    # ------------------------------------------------------------------------------------------------------------------
    def acquire_resources(self):
        """
        Acquires the resources required by this node.
        """
        for consumption in self.consumptions:
            consumption.acquire_resource()

    # ------------------------------------------------------------------------------------------------------------------
    def inquire_resources(self):
        """
        Returns true when there enough resources available to start this node. Otherwise returns false.

        :rtype: bool
        """
        ret = True

        for consumption in self.consumptions:
            ret = consumption.inquire_resource()
            if not ret:
                break

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def release_resources(self):
        """
        Releases the resources required by this node.
        """
        for consumption in self.consumptions:
            consumption.release_resource()

    # ------------------------------------------------------------------------------------------------------------------
    def _recompute_run_status(self):
        if self._predecessor_nodes:
            count_not_completed = 0
            count_not_finished = 0
            for predecessor in self._predecessor_nodes:
                if predecessor.rst_id != enarksh.ENK_RST_ID_COMPLETED:
                    count_not_completed += 1
                if predecessor.rst_id != enarksh.ENK_RST_ID_COMPLETED and \
                                predecessor.rst_id != enarksh.ENK_RST_ID_ERROR:
                    count_not_finished += 1

            if count_not_completed == 0:
                # All predecessors have run status completed.
                self._renew()
                self._set_rst_id(enarksh.ENK_RST_ID_QUEUED)

            if count_not_finished != 0 and self.rst_id != enarksh.ENK_RST_ID_WAITING:
                # A predecessors is been restarted.
                self._renew()
                self._set_rst_id(enarksh.ENK_RST_ID_WAITING)

    # ------------------------------------------------------------------------------------------------------------------
    def _set_rst_id(self, rst_id):
        """
        Sets the run status of this node.

        :param int rst_id: The new run status for this node.
        """
        old_rst_id = self.rst_id
        self._rst_id = rst_id

        # Update the start datetime of this node.
        if rst_id == enarksh.ENK_RST_ID_RUNNING:
            if not self._rnd_datetime_start:
                self._rnd_datetime_start = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            self._rnd_datetime_stop = None

        # Update the stop datetime of this node.
        if old_rst_id != rst_id and rst_id in (enarksh.ENK_RST_ID_COMPLETED, enarksh.ENK_RST_ID_ERROR):
            self._rnd_datetime_stop = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def slot_child_node_state_change(self, node, old, new):
        """
        :param node:
        :param dict old:
        :param dict new:
        """
        # Compute the running status of this complex node based on the running statuses of its child nodes.
        weight = 0
        for child_node in self._child_nodes:
            weight = max(weight, Node._rst_id_weight[child_node.rst_id])

        # Update the run status of this node.
        self._set_rst_id(self._weight_rst_id[weight])

    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def slot_predecessor_node_state_change(self, node, old, new):
        """
        :param node:
        :param dict old:
        :param dict new:
        """
        if old['rst_id'] != new['rst_id']:
            self._recompute_run_status()

    # ------------------------------------------------------------------------------------------------------------------
    def _renew(self):
        """
        If required renews this node, i.e. creates a new row in ENK_RUN_NODE.
        """
        if self.rst_id in (enarksh.ENK_RST_ID_ERROR, enarksh.ENK_RST_ID_COMPLETED):
            self._rnd_id = DataLayer.enk_back_run_node_renew(self.rnd_id)
            self._rst_id = enarksh.ENK_RST_ID_WAITING
            self._rnd_datetime_start = None
            self._rnd_datetime_stop = None
            self._exit_status = None

    # ------------------------------------------------------------------------------------------------------------------
    def initialize(self,
                   node_data,
                   schedule,
                   resources,
                   resources_data,
                   consumptions,
                   consumptions_data,
                   run_nodes,
                   child_nodes,
                   direct_predecessors,
                   direct_successors,
                   successors):
        """
        :param dict node_data:
        :param dict schedule:
        :param dict resources:
        :param dict resources_data:
        :param dict consumptions:
        :param dict consumptions_data:
        :param dict run_nodes:
        :param dict child_nodes:
        :param dict direct_predecessors:
        :param dict direct_successors:
        :param dict successors:
        """
        # Initialize the resources of this node.
        if self.rnd_id in resources_data:
            for resource_data in resources_data[self.rnd_id]:
                self.resources.append(resources[resource_data['rsc_id']])

        # Initialize the consumptions of this node.
        if self.rnd_id in consumptions_data:
            for consumption_data in consumptions_data[self.rnd_id]:
                self.consumptions.append(consumptions[consumption_data['cns_id']])

        # Observe all direct predecessor nodes of this node (for simple nodes only) and initialize predecessor state
        # count.
        if self.rnd_id in direct_predecessors:
            for predecessor in direct_predecessors[self.rnd_id]:
                node = run_nodes[predecessor]
                node.register_observer(self.slot_predecessor_node_state_change)
                self._predecessor_nodes.append(node)

        # Observe the child run_nodes of this node (for complex nodes only).
        if self.rnd_id in child_nodes:
            for child_node in child_nodes[self.rnd_id]:
                node = run_nodes[child_node['rnd_id']]
                node.register_observer(self.slot_child_node_state_change)
                self._child_nodes.append(node)

        # Set the parent node of this node.
        if node_data['rnd_id_parent']:
            self._parent_node = run_nodes[node_data['rnd_id_parent']]

        #
        if self.rnd_id in direct_successors:
            for successor in direct_successors[self.rnd_id]:
                node = run_nodes[successor]
                self._successor_nodes.append(node)

        # Set scheduling weight, i.e. the number of (direct and indirect) successors.
        if self.rnd_id in successors:
            self._scheduling_weight = len(successors[self.rnd_id])

    # ------------------------------------------------------------------------------------------------------------------
    def get_start_message(self):
        """
        :rtype: dict[str,str|int]
        """
        message = {'type': 'start_node',
                   'rnd_id': self.rnd_id}

        return message

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def restart(self):
        """
        Restarts this node.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def restart_failed(self):
        """
        Restarts all failed simple nodes.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def start(self):
        """
        :rtype: bool
        """
        # Acquire the required resources of this node.
        self.acquire_resources()

        # Set the status of this node to running.
        self._set_rst_id(enarksh.ENK_RST_ID_RUNNING)

        return True

    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def stop(self, exit_status):
        # Release all by this node consumed resources.
        self.release_resources()

        # Save the exit status of the job.
        self._exit_status = exit_status

        # Update the run status of this node based on the exit status of the job.
        if exit_status == 0:
            self._set_rst_id(enarksh.ENK_RST_ID_COMPLETED)
        else:
            self._set_rst_id(enarksh.ENK_RST_ID_ERROR)

    # ------------------------------------------------------------------------------------------------------------------
    def fake_get_resource_by_name(self, name):
        """
        Returns a resource.

        :param str name: string The name of the requested resource.

        :rtype: mixed
        """
        for resource in self.resources:
            if resource.get_name() == name:
                return resource

        if self._parent_node:
            return self._parent_node.fake_get_resource_by_name(name)

        return None

    # ------------------------------------------------------------------------------------------------------------------
    def sync_state(self):
        DataLayer.enk_back_run_node_update_status(self.rnd_id,
                                                  self.rst_id,
                                                  self._rnd_datetime_start,
                                                  self._rnd_datetime_stop,
                                                  self._exit_status)

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def is_simple_node(self):
        """
        Returns True if this node is a simple node. Otherwise, returns False.
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def get_uri(self, obj_type='node'):
        """
        Returns the URI of this node.

        :param str obj_type: The entity type.

        :rtype: str
        """
        if self._parent_node:
            uri = self._parent_node.get_uri(obj_type)
        else:
            uri = '//' + obj_type

        return uri + '/' + self._node_name

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def is_complex_node(self):
        """
        Returns True if this node is a complex node. Otherwise, returns False.
        """
        pass


# ----------------------------------------------------------------------------------------------------------------------
