"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.C import C
from enarksh.controller.node.SimpleNode import SimpleNode


class ActivateNode(SimpleNode):
    """
    Class for objects in the controller of type 'ActivateNode'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        """
        Sets the status of this node to running.

        :rtype: bool
        """
        self._exit_status = 0
        self.rst_id = C.ENK_RST_ID_RUNNING
        self.rst_id = C.ENK_RST_ID_COMPLETED

        return False

    # ------------------------------------------------------------------------------------------------------------------
    def restart_failed(self):
        """
        Raises an exception.
        """
        raise Exception("Not possible to restart an activate node")

    # ------------------------------------------------------------------------------------------------------------------
    def _renew(self):
        """
        Raises an exception.
        """
        raise Exception("Not possible to renew an activate node")

    # ------------------------------------------------------------------------------------------------------------------
    def restart(self):
        """
        Raises an exception.
        """
        raise Exception("Not possible to restart an activate node")

# ----------------------------------------------------------------------------------------------------------------------
