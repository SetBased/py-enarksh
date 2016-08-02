"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import json
from enarksh.controller.node.SimpleNode import SimpleNode


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

        :type:
        """

        self._command = json.loads(node_data['nod_command'])
        """
        The actual command of this job.

        :type:
        """

    # ------------------------------------------------------------------------------------------------------------------
    def get_start_message(self):
        message = SimpleNode.get_start_message(self)

        message['user_name'] = self._user_name
        message['args'] = self._command

        return message


# ----------------------------------------------------------------------------------------------------------------------