"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc

from enarksh.xml_reader.node.SimpleNode import SimpleNode


class ArrestNode(SimpleNode, metaclass=abc.ABCMeta):
    """
    Class for reading arrest nodes.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def is_arrest_node():
        """
        Returns true.

        :rtype: bool
        """
        return True

# ----------------------------------------------------------------------------------------------------------------------
