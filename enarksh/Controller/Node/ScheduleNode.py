"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.Controller.Node.ComplexNode import ComplexNode
from enarksh.DataLayer import DataLayer


class ScheduleNode(ComplexNode):
    """
    Class for objects in the controller of type 'Schedule'.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node_data: dict):
        ComplexNode.__init__(self, node_data)

        self._run_id = 0
        """
        The ID of the run of this schedule node.
        :type int:
        """

    # ------------------------------------------------------------------------------------------------------------------
    def initialize(self,
                   node_data: dict,
                   schedule: dict,
                   resources: dict,
                   resources_data: dict,
                   consumptions: dict,
                   consumptions_data: dict,
                   run_nodes: dict,
                   child_nodes: dict,
                   direct_predecessors: dict,
                   direct_successors: dict,
                   successors: dict) -> None:
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
