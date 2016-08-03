"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc

from enarksh.xml_reader.Dependency import Dependency


class Port(metaclass=abc.ABCMeta):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node):
        self._dependencies = []
        """
        The dependencies of this port.

        :type: list[enarksh.xml_reader.Dependency.Dependency]
        """

        self._node = node
        """
        The node (owner) of this port.

        :type: enarksh.xml_reader.node.Node.Node
        """

        self._port_name = ''
        """
        The port name of this port.

        :type: str
        """

        self._prt_id = 0
        """
        The ID of this port when it is stored in the database.

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def name(self):
        """
        Returns the name of this port.

        :rtype: str
        """
        return self._port_name

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def node(self):
        """
        Returns the node of this port.

        :rtype: enarksh.xml_reader.node.Node.Node
        """
        return self._node

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def prt_id(self):
        """
        Returns the ID of this port.

        :rtype: int
        """
        return self._prt_id

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
        if tag == 'PortName':
            self._port_name = xml.text

        elif tag == 'Dependencies':
            self._read_xml_dependencies(xml)

        else:
            raise Exception("Unexpected tag '{0!s}'.".format(tag))

    # ------------------------------------------------------------------------------------------------------------------
    def _read_xml_dependencies(self, xml):
        """
        :param xml.etree.ElementTree.Element xml:
        """
        for element in list(xml):
            tag = element.tag
            if tag == 'Dependency':
                dependency = Dependency(self)
                dependency.read_xml(element)
                self._dependencies.append(dependency)

            else:
                raise Exception("Unexpected tag '{0!s}'.".format(tag))

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self, errors):
        """
        Validates this port against rules which are not imposed by XSD.

        :param list errors: A list of error messages.
        """
        for dependency in self._dependencies:
            dependency.validate(errors)

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def store(self, nod_id):
        """
        Stores the definition of this port into the database.

        :param int nod_id: The ID of the node to which this node belongs
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def store_dependencies(self):
        """
        Stores the dependencies of this port into the database.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
