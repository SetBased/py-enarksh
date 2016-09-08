"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc


class Consumption(metaclass=abc.ABCMeta):
    """
    Abstract parent class for consumptions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node):
        self._cns_id = 0
        """
        The ID of this consumption when it is stored in the databases.

        :type: int
        """

        self._node = node
        """
        The node that owns this consumption.

        :type: enarksh.xml_reader.node.Node.Node
        """

        self._resource_name = ''
        """
        The name of the resource that is consumpted.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def get_name(self):
        """
        Returns the name of this consumption.

        :rtype: str
        """
        return self._resource_name

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
        if tag == 'ResourceName':
            self._resource_name = xml.text

        else:
            raise Exception("Unexpected tag '{0!s}'.".format(tag))

    # ------------------------------------------------------------------------------------------------------------------
    def get_uri(self, obj_type='consumption'):
        """
        Returns the URI of this consumption.

        :param str obj_type: The entity type.

        :rtype: str
        """
        if self._node:
            uri = self._node.get_uri(obj_type)
        else:
            uri = '//' + obj_type

        return uri + '/' + self._resource_name

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def store(self, nod_id):
        """
        Stores the definition of this consumption into the database.

        :param int nod_id: The ID of the node to which this consumption belongs
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
