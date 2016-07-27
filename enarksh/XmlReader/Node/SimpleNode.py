"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.XmlReader.Node.Node import Node


class SimpleNode(Node):
    # ------------------------------------------------------------------------------------------------------------------
    def get_resource_by_name(self, resource_name: str):
        """
        Returns a resource of the node.
        :param resource_name: The name of the resource.
        :return:
        """
        if self._parent_node:
            return self._parent_node.get_resource_by_name(resource_name)

        return None

    # ------------------------------------------------------------------------------------------------------------------
    def set_levels(self, recursion_level: int=0) -> None:
        """
        Sets the recursion level (i.e. the number of parent nodes) of the child nodes of this node.
        :param recursion_level: The recursion level of this node.
        """
        self._recursion_level = recursion_level
        self._dependency_level = self.get_dependency_level()


# ----------------------------------------------------------------------------------------------------------------------
