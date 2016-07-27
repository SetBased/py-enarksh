"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc
from xml.etree.ElementTree import Element

from enarksh.XmlReader.Dependency import Dependency


class Port:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node):
        self._dependencies = []
        """
        The dependencies of this port.
        """

        self._node = node
        """
        The node (owner) of this port.
        """

        self._port_name = ''
        """
        The port name of this port.
        """

        self._prt_id = 0
        """
        The ID of this port when it is stored in the database.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def get_prt_id(self) -> int:
        """
        Returns the ID of this port.
        """
        return self._prt_id

    # ------------------------------------------------------------------------------------------------------------------
    def get_name(self) -> str:
        """
        Returns the name of this port.
        """
        return self._port_name

    # ------------------------------------------------------------------------------------------------------------------
    def get_node(self):
        """
        Returns the node of this port.
        """
        return self._node

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml(self, xml: Element) -> None:
        for element in list(xml):
            self.read_xml_element(element)

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml_element(self, xml: Element) -> None:
        tag = xml.tag
        if tag == 'PortName':
            self._port_name = xml.text

        elif tag == 'Dependencies':
            self._read_xml_dependencies(xml)

        else:
            raise Exception("Unexpected tag '%s'." % tag)

    # ------------------------------------------------------------------------------------------------------------------
    def _read_xml_dependencies(self, xml: Element) -> None:
        for element in list(xml):
            tag = element.tag
            if tag == 'Dependency':
                dependency = Dependency(self)
                dependency.read_xml(element)
                self._dependencies.append(dependency)

            else:
                raise Exception("Unexpected tag '%s'." % tag)

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self, errors: list) -> None:
        """
        Validates this port against rules which are not imposed by XSD.
        :param errors: A list of error messages.
        """
        for dependency in self._dependencies:
            dependency.validate(errors)

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def store(self, nod_id: int) -> None:
        """
        Stores the definition of this port into the database.
        :param nod_id: The ID of the node to which this node belongs
        """
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def store_dependencies(self) -> None:
        """
        Stores the dependencies of this port into the database.
        """
        pass

# ----------------------------------------------------------------------------------------------------------------------
