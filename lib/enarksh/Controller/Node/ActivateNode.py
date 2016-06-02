from lib import enarksh
from lib.enarksh.Controller.StateChange import StateChange
from lib.enarksh.Controller.Node.SimpleNode import SimpleNode


# ----------------------------------------------------------------------------------------------------------------------
class ActivateNode(SimpleNode):
    """
    Class for objects in the controller of type 'ActivateNode'.
    """
    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def start(self):
        # Set the status of this node to running.
        self.rst_id = enarksh.ENK_RST_ID_RUNNING

        return False

    # ------------------------------------------------------------------------------------------------------------------
    def restart_failed(self) -> None:
        """
        Raises an exception.
        """
        raise Exception("Not possible to restart an activate node")

    # ------------------------------------------------------------------------------------------------------------------
    def _renew(self) -> None:
        """
        Raises an exception.
        """
        raise Exception("Not possible to renew an activate node")

    # ------------------------------------------------------------------------------------------------------------------
    def restart(self) -> None:
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
