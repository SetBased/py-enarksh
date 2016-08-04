"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.DataLayer import DataLayer


class Dependency:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, port):
        self._node_name = ''
        """
        The name of the referenced node of this dependency.

        :type: str
        """

        self._port = port
        """
        The port (owner) of this dependency.

        :type: enarksh.xml_reader.port.Port.Port
        """

        self._port_name = ''
        """
        The name of the referenced port of this dependency.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def get_dependency_level(self):
        """
        :rtype: int
        """
        if self._node_name == '.':
            return -1
        else:
            return self._port.node.parent_node.get_node_by_name(self._node_name).get_dependency_level()

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml(self, xml):
        """
        :param xml.etree.ElementTree.Element xml:
        """
        for element in list(xml):
            tag = element.tag
            if tag == 'NodeName':
                self._node_name = element.text

            elif tag == 'PortName':
                self._port_name = element.text

            else:
                raise RuntimeError("Unexpected tag '{0!s}'.".format(tag))

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self, errors):
        """
        Validates this dependency against rules which are not imposed by XSD.

        :param list errors: A list of error messages.
        """
        # @todo XXX Node named $this->myNodeName must exists.
        # @todo XXX Node must have port named $this->myPortName.
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def store(self, port, node):
        """
        Stores this dependency into the database.

        :param enarksh.xml_reader.port.Port.Port port: The port of the dependency.
        :param enarksh.xml_reader.node.Node.Node node: The node of the dependency.
        """
        prt_id_dependant = port.prt_id
        prt_id_predecessor = node.get_port_by_name(self._node_name, self._port_name).prt_id

        DataLayer.enk_reader_dependency_store_dependency(prt_id_dependant, prt_id_predecessor)

# ----------------------------------------------------------------------------------------------------------------------
