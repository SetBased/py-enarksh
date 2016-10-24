"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import enarksh
from enarksh.controller.node.Node import Node


class ComplexNode(Node):
    """
    Class for objects in the controller of type 'ComplexJob'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def is_simple_node(self):
        """
        Returns False.

        :rtype: bool
        """
        return False

    # ------------------------------------------------------------------------------------------------------------------
    def is_complex_node(self):
        """
        Returns True.

        :rtype: bool
        """
        return True

    # ------------------------------------------------------------------------------------------------------------------
    def restart(self):
        """
        Restart this node. I.e. makes a new run node (if the run node has run before) and set the run status to
        waiting.
        """
        self._renew()

        for child in self._child_nodes:
            child.restart()

    # ------------------------------------------------------------------------------------------------------------------
    def restart_failed(self):
        """
        Restarts the failed child nodes of this node.
        """
        for child in self._child_nodes:
            # If child is a simple node and its status is ENK_RST_ID_ERROR restart this node.
            if child.is_simple_node():
                if child.rst_id == enarksh.ENK_RST_ID_ERROR:
                    child.restart_failed()

            # If child is a complex node cascade the process of restarting failed nodes.
            if child.is_complex_node():
                child.restart_failed()

# ----------------------------------------------------------------------------------------------------------------------
