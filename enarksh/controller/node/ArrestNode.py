"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.C import C
from enarksh.controller.node.SimpleNode import SimpleNode


class ArrestNode(SimpleNode):
    """
    Class for objects in the controller of type 'ArrestNode'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def start(self):
        self._exit_status = 0
        self.rst_id = C.ENK_RST_ID_RUNNING
        self.rst_id = C.ENK_RST_ID_COMPLETED

        return False

# ----------------------------------------------------------------------------------------------------------------------
