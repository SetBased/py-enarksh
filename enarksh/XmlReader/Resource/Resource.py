import abc
from xml.etree.ElementTree import Element


class Resource:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node):
        self._node = node
        """
        The node that owns this resource.
        """

        self._resource_name = ''
        """
        The name of this resource.
        :type str:
        """

        self._rsc_id = 0
        """
        The ID of this resource when it is stored in the databases.
        :type int:
        """

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
            Resource.read_xml_element(self, xml)

    # ------------------------------------------------------------------------------------------------------------------
    def get_rsc_id(self) -> str:
        """
        Returns the ID of this resource.
        """
        return self._rsc_id

    # ------------------------------------------------------------------------------------------------------------------
    def get_name(self) -> str:
        """
        Returns the name of this resource.
        """
        return self._resource_name

    # ------------------------------------------------------------------------------------------------------------------
    def get_uri(self, obj_type: str='resource') -> str:
        """
        Returns the URI of this resource.
        :param obj_type: The entity type.
        """
        if self._node:
            uri = self._node.get_uri(obj_type)
        else:
            uri = '//' + obj_type

        return uri + '/' + self._resource_name

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def store(self, hst_id: int, nod_id: int) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self, errors: list) -> None:
        """
        Validates this resource against rules which are not imposed by XSD.
        :param errors: A list of error messages.
        """
        # Nothing to do.


# ----------------------------------------------------------------------------------------------------------------------
