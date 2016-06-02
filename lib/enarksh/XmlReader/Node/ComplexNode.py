from pydoc import locate

from lxml.etree import Element

from lib.enarksh.XmlReader.Node.Node import Node
from lib.enarksh.XmlReader.Resource import CountingResource, ReadWriteLockResource


# ----------------------------------------------------------------------------------------------------------------------
class ComplexNode(Node):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent_node=None):
        Node.__init__(self, parent_node)

        self._child_nodes = {}
        """
        The child nodes of this node.
        :type dict:
        """

        self._resources = {}
        """
        The resources of this node.
        :type dict:
        """

    # ------------------------------------------------------------------------------------------------------------------
    def store_dependencies(self) -> None:
        """
        Stores the dependencies of this node into the database.
        """
        Node.store_dependencies(self)

        # Store the dependencies of the ports of the child nodes of this node.
        for child_node in self._child_nodes.values():
            child_node.store_dependencies()

    # ------------------------------------------------------------------------------------------------------------------
    def store(self, srv_id: int, p_nod_master: int) -> None:
        """
        Stores the definition of this node into the database.
        :param srv_id: The ID of the schedule revision to which this node belongs.
        """
        Node.store(self, srv_id, p_nod_master)

        # Store the resources of this node.
        for resource in self._resources.values():
            resource.store(None, self._nod_id)

        # Store the child nodes of this node.
        for child_node in self._child_nodes.values():
            child_node.store(srv_id, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    def get_node_by_name(self, node_name):
        """
        Return a child node of this node.
        """
        if node_name == '.':
            return self

        return self._child_nodes[node_name]

    # ------------------------------------------------------------------------------------------------------------------
    def set_levels(self, recursion_level: int=0) -> None:
        """
        Sets the recursion level (i.e. the number of parent nodes) of the child nodes of this node.
        :param recursion_level: The recursion level of this node.
        """
        self._recursion_level = recursion_level
        for child_node in self._child_nodes.values():
            child_node.set_levels(recursion_level + 1)

        self._dependency_level = self.get_dependency_level()

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_helper(self, errors: list) -> None:
        """
        Helper function for validation this node.
        :param errors: A list of error messages.
        """
        Node._validate_helper(self, errors)

        # Validate all resources.
        for resource in self._resources.values():
            resource.validate(errors)

        # Validate all child nodes.
        for node in self._child_nodes.values():
            node._validate_helper(errors)

        # @todo Validate no circular references exists.

    # ------------------------------------------------------------------------------------------------------------------
    def get_resource_by_name(self, resource_name: str):
        """
        Returns a resource of the node.
        :param resource_name: The name of the resource.
        :return:
        """
        if resource_name in self._resources:
            return self._resources[resource_name]

        if self._parent_node:
            return self._parent_node.get_resource_by_name(resource_name)

        return None

    # ------------------------------------------------------------------------------------------------------------------
    def _read_xml_nodes(self, xml: Element) -> None:
        for element in list(xml):
            module = locate('lib.enarksh.XmlReader.Node')
            node = module.create_node(element.tag, self)
            node.read_xml(element)
            name = node._node_name

            # Check for child nodes with duplicate names.
            if name in self._child_nodes:
                raise Exception("Duplicate child node '%s'." % name)

            # Add child node to map of child nodes.
            self._child_nodes[name] = node

    # ------------------------------------------------------------------------------------------------------------------
    def _read_xml_resources(self, xml: Element) -> None:
        for element in list(xml):
            tag = element.tag
            if tag == 'CountingResource':
                resource = CountingResource(self)

            elif tag == 'ReadWriteLockResource':
                resource = ReadWriteLockResource(self)

            else:
                raise Exception("Unexpected tag '%s'." % tag)

            resource.read_xml(element)
            name = resource.get_name()
            # Check for resources with duplicate names.
            if name in self._resources:
                raise Exception("Duplicate resource '%s'." % name)

            self._resources[name] = resource

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml_element(self, xml: Element) -> None:
        tag = xml.tag
        if tag == 'Resources':
            self._read_xml_resources(xml)

        elif tag == 'Nodes':
            self._read_xml_nodes(xml)

        else:
            Node.read_xml_element(self, xml)


# ----------------------------------------------------------------------------------------------------------------------
