"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from pydoc import locate

from enarksh.DataLayer import DataLayer
from enarksh.xml_reader.node.Node import Node


class DynamicJobNode(Node):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent_node=None):
        Node.__init__(self, parent_node)

        self._generator = None
        """
        :type: Node
        """

        self._worker = None
        """
        :type: Node
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _store_self(self, srv_id, uri_id, p_nod_master):
        """
        Stores the definition of this node into the database.

        :param int srv_id: The ID of the schedule to which this node belongs.
        :param int uri_id: The ID of the URI of this node.
        :param int p_nod_master:
        """
        self._nod_id = DataLayer.enk_reader_node_store_dynamic_job(srv_id,
                                                                   uri_id,
                                                                   self._parent_node._nod_id,
                                                                   self._node_name,
                                                                   self._recursion_level,
                                                                   self._dependency_level,
                                                                   p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    def get_resource_by_name(self, resource_name):
        """
        :param str resource_name:

        :rtype: str
        """
        # A dynamic doesn't have resources.
        return self._parent_node.get_resource_by_name(resource_name)

    # ------------------------------------------------------------------------------------------------------------------
    def store_dependencies(self):
        """
        Stores the dependencies of this node into the database.
        """
        Node.store_dependencies(self)

        # Store the dependencies of the ports of the child nodes of this node.
        self._generator.store_dependencies()
        self._worker.store_dependencies()

    # ------------------------------------------------------------------------------------------------------------------
    def store(self, srv_id, p_nod_master):
        """
        Stores the definition of this node into the database.

        :param int srv_id: The ID of the schedule revision to which this node belongs.
        :param int p_nod_master:
        """
        Node.store(self, srv_id, p_nod_master)

        self._generator.store(srv_id, p_nod_master)
        self._worker.store(srv_id, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    def set_levels(self, recursion_level=0):
        """
        Sets the recursion level (i.e. the number of parent nodes) of the child nodes of this node.

        :param int recursion_level: The recursion level of this node.
        """
        self._recursion_level = recursion_level

        self._generator.set_levels(recursion_level + 1)
        self._worker.set_levels(recursion_level + 1)

        self._dependency_level = self.get_dependency_level()

    # ------------------------------------------------------------------------------------------------------------------
    def _read_xml_generator(self, xml):
        """
        :param lxml.etree.Element xml:
        """
        module = locate('enarksh.xml_reader.node')
        node = module.create_node('CommandJob', self)
        node.read_xml(xml)

        # Add child node to map of child nodes.
        self._generator = node

    # ------------------------------------------------------------------------------------------------------------------
    def _read_xml_worker(self, xml):
        """
        :param lxml.etree.Element xml:
        """
        module = locate('enarksh.xml_reader.node')
        node = module.create_node('DynamicOuterWorker', self)
        node.read_xml(xml)

        # Add child node to map of child nodes.
        self._worker = node

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml_element(self, xml):
        """
        :param lxml.etree.Element xml:
        """
        tag = xml.tag
        if tag == 'Generator':
            self._read_xml_generator(xml)

        elif tag == 'Worker':
            self._read_xml_worker(xml)

        else:
            Node.read_xml_element(self, xml)

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_helper(self, errors):
        """
        Helper function for validation this node.

        :param list errors: A list of error messages.
        """
        Node._validate_helper(self, errors)

        self._generator._validate_helper(errors)
        self._worker._validate_helper(errors)

        # @todo Validate no circular references exists.

    # ------------------------------------------------------------------------------------------------------------------
    def get_node_by_name(self, node_name):
        """
        Return a child node of this node.

        :param str node_name:

        :rtype: mixed
        """
        if node_name == '.':
            return self

        if node_name == self._generator._node_name:
            return self._generator

        if node_name == self._worker._node_name:
            return self._worker

        raise Exception("Unknown node '{0!s}'.".format(node_name))

# ----------------------------------------------------------------------------------------------------------------------
