"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import enarksh
from enarksh.Controller.StateChange import StateChange
from enarksh.Controller.Node.SimpleNode import SimpleNode


class ActivateNode(SimpleNode):
    """
    Class for objects in the controller of type 'ActivateNode'.
    """
    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def start(self):
        """
        Sets the status of this node to running.

        :rtype: bool
        """
        self.rst_id = enarksh.ENK_RST_ID_RUNNING

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

    # ------------------------------------------------------------------------------------------------------------------
    def get_start_message(self):
        """
        Raises an exception.
        """
        raise Exception("Internal error.")

# ----------------------------------------------------------------------------------------------------------------------
