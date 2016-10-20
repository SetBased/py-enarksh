"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from cleo import Command

import enarksh
from enarksh.controller.client.NodeActionClient import NodeActionClient
from enarksh.style.EnarkshStyle import EnarkshStyle


class NodeActionCommand(Command):
    """
    Requests the controller for a node action

    node_action
        {action : The action: trigger, restart, or restart_failed}
        {uri : The URI of the node}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the request node action command.
        """
        self.output = EnarkshStyle(self.input, self.output)

        action = self.input.get_argument('action')
        if action == 'trigger':
            act_id = enarksh.ENK_ACT_ID_TRIGGER
        elif action == 'restart':
            act_id = enarksh.ENK_ACT_ID_RESTART
        elif action == 'restart_failed':
            act_id = enarksh.ENK_ACT_ID_RESTART_FAILED
        else:
            raise RuntimeError("Unknown action '{}'".format(action))

        uri = self.input.get_argument('uri')

        client = NodeActionClient(self.output)
        ret = client.main(uri, act_id)

        return ret

# ----------------------------------------------------------------------------------------------------------------------
