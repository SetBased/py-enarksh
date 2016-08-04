"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc

from enarksh.DataLayer import DataLayer
from enarksh.xml_reader.consumption.CountingConsumption import CountingConsumption
from enarksh.xml_reader.consumption.ReadWriteLockConsumption import ReadWriteLockConsumption
from enarksh.xml_reader.port.InputPort import InputPort
from enarksh.xml_reader.port.OutputPort import OutputPort


class Node(metaclass=abc.ABCMeta):
    # ------------------------------------------------------------------------------------------------------------------
    """
    Abstract class for parsing XML definition of nodes.
    """

    def __init__(self, parent_node=None):
        self._node_name = ''
        """
        The name of this node.

        :type: str
        """

        self._user_name = ''
        """
        The user under which this node or its child nodes must run.

        :type: str
        """

        self._input_ports = {}
        """
        The input ports of this node.

        :type: dict
        """

        self._output_ports = {}
        """
        The output ports of this node.

        :type: dict
        """

        self._consumptions = {}
        """
        The consumptions of this node.

        :type: dict
        """

        self._nod_id = 0
        """
        The ID of this node when it is stored in the database.

        :type: int
        """

        self._parent_node = parent_node
        """
        The parent node of this node.

        :type: Node
        """

        self._recursion_level = -1
        """
        The recursion level of this node. I.e. the total number of (recursive) parent nodes.

        :type: int
        """

        self._dependency_level = -1
        """
        The dependency level of this node. I.e. the number of predecessors of this node (with the parent node).

        :type: int
        """

        self._user_name = ''
        """
        The user under which this node or its child nodes must run.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def name(self):
        """
        Returns the name of this node.

        :rtype: str
        """
        return self._node_name

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def nod_id(self):
        """
        Returns the ID of this node.

        :rtype: int
        """
        return self._nod_id

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def parent_node(self):
        """
        Returns the parent node of this node.

        :rtype: Node
        """
        return self._parent_node

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml(self, xml):
        """
        :param xml.etree.ElementTree.Element xml:
        """
        for element in list(xml):
            self.read_xml_element(element)

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml_element(self, xml):
        """
        :param xml.etree.ElementTree.Element xml:
        """
        tag = xml.tag
        if tag == 'NodeName':
            self._node_name = xml.text

        elif tag == 'UserName':
            self._user_name = xml.text

        elif tag == 'InputPorts':
            self._read_xml_input_ports(xml)

        elif tag == 'Consumptions':
            self._read_xml_consumptions(xml)

        elif tag == 'OutputPorts':
            self._read_xml_output_ports(xml)

        else:
            raise Exception("Unexpected tag '{0!s}'.".format(tag))

    # ------------------------------------------------------------------------------------------------------------------
    def _read_xml_consumptions(self, xml):
        """
        :param xml.etree.ElementTree.Element xml:
        """
        for element in list(xml):
            tag = element.tag
            if tag == 'CountingConsumption':
                consumption = CountingConsumption(self)

            elif tag == 'ReadWriteLockConsumption':
                consumption = ReadWriteLockConsumption(self)

            else:
                raise Exception("Unexpected tag '{0!s}'.".format(tag))

            consumption.read_xml(element)
            name = consumption.get_name()
            # Check for consumptions with duplicate names.
            if name in self._consumptions:
                raise Exception("Duplicate consumption '{0!s}'.".format(name))

            self._consumptions[name] = consumption

    # ------------------------------------------------------------------------------------------------------------------
    def _read_xml_input_ports(self, xml):
        """
        :param xml.etree.ElementTree.Element xml:
        """
        for element in list(xml):
            tag = element.tag
            if tag == 'Port':
                port = InputPort(self)
                port.read_xml(element)

                name = port.name
                # Check for ports with duplicate names.
                if name in self._input_ports:
                    raise Exception("Duplicate input port '{0!s}'.".format(name))

                self._input_ports[name] = port

            else:
                raise Exception("Unexpected tag '{0!s}'.".format(tag))

    # ------------------------------------------------------------------------------------------------------------------
    def _read_xml_output_ports(self, xml):
        """
        :param xml.etree.ElementTree.Element xml:
        """
        for element in list(xml):
            tag = element.tag
            if tag == 'Port':
                port = OutputPort(self)
                port.read_xml(element)

                name = port.name
                # Check for ports with duplicate names.
                if name in self._output_ports:
                    raise Exception("Duplicate output port '{0!s}'.".format(name))

                self._output_ports[name] = port

            else:
                raise Exception("Unexpected tag '{0!s}'.".format(tag))

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_resource_by_name(self, resource_name):
        """
        Returns a resource of the node.

        :param str resource_name: The name of the resource.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def is_activate_node():
        """
        Returns true if this node is a ActivateNode. Otherwise return false.

        :rtype: bool
        """
        return False

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def is_arrest_node():
        """
        Returns true if this node is a ActivateNode. Otherwise return false.

        :rtype: bool
        """
        return False

    # ------------------------------------------------------------------------------------------------------------------
    def get_dependency_level(self):
        """
        Returns the dependency level (i.e. the number of predecessors of this node within the parent node) of this node.

        :rtype: int
        """
        if self._dependency_level == -1:
            self._dependency_level = 0
            for port in self._input_ports.values():
                level = port.get_dependency_level()
                if level >= self._dependency_level:
                    self._dependency_level = level + 1

        return self._dependency_level

    # ------------------------------------------------------------------------------------------------------------------
    def get_uri(self, obj_type='node'):
        """
        Returns the URI of this node.

        :param str obj_type: The entity type.

        :rtype: str
        """
        if self._parent_node:
            uri = self._parent_node.get_uri(obj_type)
        else:
            uri = '//' + obj_type

        return uri + '/' + self._node_name

    # ------------------------------------------------------------------------------------------------------------------
    def get_user_name(self):
        """
        Returns the user name under which this node must run.

        :rtype: str
        """
        if self._user_name:
            return self._user_name

        if self._parent_node:
            self._user_name = self._parent_node.get_user_name()

        return self._user_name

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self, fake_parent=None):
        """
        Validates this node against rules which are not imposed by XSD.

        :param fake_parent:

        :rtype: str
        """
        self._parent_node = fake_parent

        errors = []
        """:type errors: list[dict[str,str]]"""
        self._validate_helper(errors)

        if errors:
            message = ''
            for error in errors:
                message += 'URI:   ' + error['uri'] + '\n'
                message += 'Rule:  ' + error['rule'] + '\n'
                message += 'Error: ' + error['error'] + '\n'

            return message

        return ''

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_helper(self, errors):
        """
        Helper function for validation this node.

        :param list[dict[str,str]] errors: A list of error messages.
        """
        # Validate all input ports.
        for port in self._input_ports.values():
            port.validate(errors)

        # Validate all consumptions.
        for consumption in self._consumptions.values():
            consumption.validate(errors)

        # @todo Validate no circular references exists.

        # Validate all output ports.
        for port in self._output_ports.values():
            port.validate(errors)

    # ------------------------------------------------------------------------------------------------------------------
    def store(self, srv_id, p_nod_master):
        """
        Stores the definition of this node into the database.

        :param int srv_id: The ID of the schedule revision to which this node belongs.
        :param int p_nod_master:
        """
        # Get uri_id for this node.
        uri_id = DataLayer.enk_misc_insert_uri(self.get_uri())

        # Store the definition of the node self.
        self._store_self(srv_id, uri_id, p_nod_master)

        # Store the consumptions of this node.
        for consumption in self._consumptions.values():
            consumption.store(self._nod_id)

        # Store the input ports of this node.
        for port in self._input_ports.values():
            port.store(self._nod_id)

        # Store the output ports of this node.
        for port in self._output_ports.values():
            port.store(self._nod_id)

    # ------------------------------------------------------------------------------------------------------------------
    def get_port_by_name(self, node_name, port_name):
        """
        Return an output port of a child node of this node or an input port this node.

        :param str node_name:
        :param str port_name:

        :rtype: enarksh.xml_reader.port.Port.Port
        """
        if node_name == '.':
            return self._input_ports[port_name]

        node = self.get_node_by_name(node_name)

        return node._output_ports[port_name]

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_node_by_name(self, node_name):
        """
        Returns a child node of this node by name.

        :param str node_name: The name of the searched child node.

        :rtype: enarksh.xml_reader.Node.Node.Node
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def store_dependencies(self):
        """
        Stores the dependencies of this node into the database.
        """
        # Store the dependencies of the input ports of this node.
        for port in self._input_ports.values():
            port.store_dependencies()

        # Store the dependencies of the output ports of this node.
        for port in self._output_ports.values():
            port.store_dependencies()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def set_levels(self, recursion_level=0):
        """
        Sets the recursion level (i.e. the number of parent nodes) of the child nodes of this node.

        :param int recursion_level: The recursion level of this node.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _store_self(self, srv_id, uri_id, p_nod_master):
        """
        Stores the definition of this node into the database.

        :param int srv_id: The ID of the schedule to which this node belongs.
        :param int uri_id: The ID of the URI of this node.
        :param int p_nod_master:
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
