"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from xml.etree.ElementTree import Element

from enarksh.DataLayer import DataLayer


class Dependency:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, port):
        self._node_name = ''
        """
        The name of the referenced node of this dependency.
        """

        self._port = port
        """
        The port (owner) of this dependency.
        :type: Port
        """

        self._port_name = ''
        """
        The name of the referenced port of this dependency.
        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def get_dependency_level(self) -> int:
        if self._node_name == '.':
            return -1
        else:
            return self._port.get_node().get_parent_node().get_node_by_name(self._node_name).get_dependency_level()

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml(self, xml: Element) -> None:
        for element in list(xml):
            tag = element.tag
            if tag == 'NodeName':
                self._node_name = element.text

            elif tag == 'PortName':
                self._port_name = element.text

            else:
                raise Exception("Unexpected tag '{0!s}'.".format(tag))

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self, errors: list) -> None:
        """
        Validates this dependency against rules which are not imposed by XSD.
        :param errors: A list of error messages.
        """
        # XXX Node named $this->myNodeName must exists.
        # XXX Node must have port named $this->myPortName.

    # ------------------------------------------------------------------------------------------------------------------
    def store(self, port, node) -> None:
        prt_id_dependant = port.get_prt_id()
        prt_id_predecessor = node.get_port_by_name(self._node_name, self._port_name).get_prt_id()

        DataLayer.enk_reader_dependency_store_dependency(prt_id_dependant, prt_id_predecessor)


# ----------------------------------------------------------------------------------------------------------------------
