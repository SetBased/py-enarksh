"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import enarksh
from enarksh.controller.node.Node import Node


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
    def start(self):
        """
        Does the housekeeping for starting this node. Returns True if an actual job must be started by the spawner.
        Returns False otherwise.

        :rtype: bool
        """
        # Acquire the required resources of this node.
        self.acquire_resources()

        # Set the status of this node to running.
        self.rst_id = enarksh.ENK_RST_ID_RUNNING

        return True

    # ------------------------------------------------------------------------------------------------------------------
    def stop(self, exit_status):
        """
        Does the housekeeping when the node has stopped.

        :param int exit_status: The exits status of the job.
        """
        # Release all by this node consumed resources.
        self.release_resources()

        # Save the exit status of the job.
        self._exit_status = exit_status

        # Update the run status of this node based on the exit status of the job.
        if exit_status == 0:
            self.rst_id = enarksh.ENK_RST_ID_COMPLETED
        else:
            self.rst_id = enarksh.ENK_RST_ID_ERROR

    # ------------------------------------------------------------------------------------------------------------------
    def restart(self):
        """
        Restart this node and its successors.
        """
        if self._rst_id in (enarksh.ENK_RST_ID_ERROR, enarksh.ENK_RST_ID_COMPLETED):
            self._renew()
            self._recompute_run_status()

    # ------------------------------------------------------------------------------------------------------------------
    def restart_failed(self):
        """
        Restart this node.
        """
        if self._rst_id == enarksh.ENK_RST_ID_ERROR:
            self._renew()
            self._recompute_run_status()
        else:
            raise Exception("Not possible to restart node with rst_id '{0!s}'.".format(self.rst_id))

# ----------------------------------------------------------------------------------------------------------------------
