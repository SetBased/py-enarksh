"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc
from xml.etree.ElementTree import Element


class Consumption:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node):
        self._cns_id = 0
        """
        The ID of this consumption when it is stored in the databases.
        :type int:
        """

        self._node = node
        """
        The node that owns this consumption.
        """

        self._resource_name = ''
        """
        The name of the resource that is consumpted.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def get_name(self) -> str:
        """
        Returns the name of this consumption.
        """
        return self._resource_name

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml(self, xml: Element) -> None:
        for element in list(xml):
            self.read_xml_element(element)

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml_element(self, xml: Element) -> None:
        tag = xml.tag
        if tag == 'ResourceName':
            self._resource_name = xml.text

        else:
            raise Exception("Unexpected tag '{0!s}'.".format(tag))

    # ------------------------------------------------------------------------------------------------------------------
    def get_uri(self, obj_type: str='consumption') -> str:
        """
        Returns the URI of this consumption.
        :param obj_type: The entity type.
        """
        if self._node:
            uri = self._node.get_uri(obj_type)
        else:
            uri = '//' + obj_type

        return uri + '/' + self._resource_name

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def store(self, nod_id: int) -> None:
        """
        Stores the definition of this consumption into the database.
        :param nod_id: The ID of the node to which this consumption belongs
        """
        pass


# ----------------------------------------------------------------------------------------------------------------------
