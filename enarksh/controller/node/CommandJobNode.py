"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import json

from enarksh.controller.node.SimpleNode import SimpleNode
from enarksh.spawner.message.SpawnJobMessage import SpawnJobMessage


class CommandJobNode(SimpleNode):
    """
    Class for objects in the controller of type 'CommandJob'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node_data):
        """
        Object constructor

        :param dict node_data:
        """
        SimpleNode.__init__(self, node_data)

        self._user_name = node_data['nod_user_name']
        """
        The account under which the command must run.

        :type: str
        """

        self._command = json.loads(node_data['nod_command'])
        """
        The actual command of this job.

        :type: list[str]
        """

    # ------------------------------------------------------------------------------------------------------------------
    def get_start_message(self, sch_id):
        """
        Returns the message to be send to the spawner for starting this node.

        :param int sch_id: The ID of the schedule.

        :rtype: enarksh.message.Message.Message
        """
        return SpawnJobMessage(sch_id, self.rnd_id, self._user_name, self._command)

# ----------------------------------------------------------------------------------------------------------------------
