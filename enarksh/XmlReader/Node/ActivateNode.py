"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.XmlReader.Node.SimpleNode import SimpleNode


class ActivateNode(SimpleNode):
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def is_activate_node():
        """
        Returns true.

        :rtype: bool
        """
        return True


# ----------------------------------------------------------------------------------------------------------------------
