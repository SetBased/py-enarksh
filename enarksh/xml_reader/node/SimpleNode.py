"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc

from enarksh.xml_reader.node.Node import Node


class SimpleNode(Node, metaclass=abc.ABCMeta):
    # ------------------------------------------------------------------------------------------------------------------
    def get_node_by_name(self, node_name):
        """
        Raise an exception. A simple node does not have child nodes.

        :param str node_name: The name of the child node.
        """
        raise ValueError("Can not find child node '{}'".format(node_name))

    # ------------------------------------------------------------------------------------------------------------------
    def get_resource_by_name(self, resource_name):
        """
        Returns a resource of the node.

        :param str resource_name: The name of the resource.

        :rtype: mixed
        """
        if self._parent_node:
            return self._parent_node.get_resource_by_name(resource_name)

        return None

    # ------------------------------------------------------------------------------------------------------------------
    def set_levels(self, recursion_level=0):
        """
        Sets the recursion level (i.e. the number of parent nodes) of the child nodes of this node.

        :param int recursion_level: The recursion level of this node.
        """
        self._recursion_level = recursion_level
        self._dependency_level = self.get_dependency_level()

# ----------------------------------------------------------------------------------------------------------------------
