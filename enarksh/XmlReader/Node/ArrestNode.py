"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc

from enarksh.XmlReader.Node.SimpleNode import SimpleNode


class ArrestNode(metaclass=abc.ABCMeta, SimpleNode):
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def is_arrest_node():
        """
        Returns true.

        :rtype: bool
        """
        return True

# ----------------------------------------------------------------------------------------------------------------------
