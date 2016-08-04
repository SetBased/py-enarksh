"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc


class Resource(metaclass=abc.ABCMeta):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node):
        self._node = node
        """
        The node that owns this resource.

        :type: enarksh.xml_reader.node.Node.Node
        """

        self._resource_name = ''
        """
        The name of this resource.

        :type: str
        """

        self._rsc_id = 0
        """
        The ID of this resource when it is stored in the databases.

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def name(self):
        """
        Returns the name of this resource.

        :rtype: str
        """
        return self._resource_name

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def rsc_id(self):
        """
        Returns the ID of this resource.

        :rtype: str
        """
        return self._rsc_id

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
            Resource.read_xml_element(self, xml)

    # ------------------------------------------------------------------------------------------------------------------
    def get_uri(self, obj_type='resource'):
        """
        Returns the URI of this resource.

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
    def store(self, hst_id, nod_id):
        """
        :param int|None hst_id: The ID of the host.
        :param int|Node nod_id: The ID of the node.

        :rtype: None
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self, errors):
        """
        Validates this resource against rules which are not imposed by XSD.

        :param list errors: A list of error messages.
        """
        pass

# ----------------------------------------------------------------------------------------------------------------------
