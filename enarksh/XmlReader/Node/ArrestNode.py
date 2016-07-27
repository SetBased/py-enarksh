"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.XmlReader.Node.SimpleNode import SimpleNode


class ArrestNode(SimpleNode):
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def is_arrest_node() -> bool:
        """
        Returns true.
        """
        return True

# ----------------------------------------------------------------------------------------------------------------------
