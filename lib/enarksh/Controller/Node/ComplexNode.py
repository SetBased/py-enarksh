from lib import enarksh
from lib.enarksh.Controller.StateChange import StateChange
from lib.enarksh.Controller.Node.Node import Node


# ----------------------------------------------------------------------------------------------------------------------
class ComplexNode(Node):
    """
    Class for objects in the controller of type 'ComplexJob'.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def is_simple_node(self) -> bool:
        """
        Returns False.
        """
        return False

    # ------------------------------------------------------------------------------------------------------------------
    def is_complex_node(self) -> bool:
        """
        Returns True.
        """
        return True

    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def restart(self) -> None:
        """
        Restart this node. I.e. makes a new run node (if the run node has run before) and set the run status to
        waiting.
        """
        self._renew()

        for child in self._child_nodes:
            child.restart()

    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def restart_failed(self) -> None:
        """
        Restarts the failed child nodes of this node.
        """
        for child in self._child_nodes:
            # If child is a simple node and its status is ENK_RST_ID_ERROR restart this node.
            if child.is_simple_node():
                if child.get_rst_id() == enarksh.ENK_RST_ID_ERROR:
                    child.restart_failed()

            # If child is a complex node cascade the process of restarting failed nodes.
            if child.is_complex_node():
                child.restart_failed()


# ----------------------------------------------------------------------------------------------------------------------
