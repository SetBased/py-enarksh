"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.DataLayer import DataLayer
from enarksh.controller.node.ComplexNode import ComplexNode


class ScheduleNode(ComplexNode):
    """
    Class for objects in the controller of type 'Schedule'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node_data):
        """
        Object constructor.

        :param dict node_data:
        """
        ComplexNode.__init__(self, node_data)

        self._run_id = 0
        """
        The ID of the run of this schedule node.

        :type: int
        """

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
        ComplexNode.initialize(self,
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
                               successors)

        self._run_id = schedule['run_id']

    # ------------------------------------------------------------------------------------------------------------------
    def sync_state(self):
        ComplexNode.sync_state(self)

        DataLayer.enk_back_run_update_status(self._run_id, self._rnd_datetime_start, self._rnd_datetime_stop)

# ----------------------------------------------------------------------------------------------------------------------
