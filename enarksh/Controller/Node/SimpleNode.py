"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import enarksh
from enarksh.Controller.StateChange import StateChange
from enarksh.Controller.Node.Node import Node


class SimpleNode(Node):
    """
    Class for objects in the controller of type 'SimpleJob'.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def is_simple_node(self):
        """
        Returns True.

        :rtype: bool
        """
        return True

    # ------------------------------------------------------------------------------------------------------------------
    def is_complex_node(self):
        """
        Returns False.

        :rtype: bool
        """
        return False

    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def restart(self):
        """
        Restart this node and its successors.
        """
        if self.rst_id in (enarksh.ENK_RST_ID_ERROR, enarksh.ENK_RST_ID_COMPLETED):
            self._renew()
            self._recompute_run_status()

    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def restart_failed(self):
        """
        Restart this node.
        """
        if self.rst_id == enarksh.ENK_RST_ID_ERROR:
            self._renew()
            self._recompute_run_status()

        else:
            raise Exception("Not possible to restart node with rst_id '{0!s}'.".format(self.rst_id))

# ----------------------------------------------------------------------------------------------------------------------
