"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import enarksh
from enarksh.controller.StateChange import StateChange
from enarksh.controller.node.SimpleNode import SimpleNode


class ArrestNode(SimpleNode):
    """
    Class for objects in the controller of type 'ArrestNode'.
    """
    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def start(self):
        self._set_rst_id(enarksh.ENK_RST_ID_COMPLETED)

        return False

    # ------------------------------------------------------------------------------------------------------------------
    def get_start_message(self):
        raise Exception("Internal error.")


# ----------------------------------------------------------------------------------------------------------------------
