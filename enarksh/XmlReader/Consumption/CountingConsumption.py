"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from xml.etree.ElementTree import Element

from enarksh.DataLayer import DataLayer

from enarksh.XmlReader.Consumption.Consumption import Consumption


class CountingConsumption(Consumption):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node):
        Consumption.__init__(self, node)

        self._amount = 0
        """
        The amount that will be consumpted.

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml_element(self, xml):
        """
        :param xml.etree.ElementTree.Element xml:
        """
        tag = xml.tag
        if tag == 'Amount':
            self._amount = int(xml.text)

        else:
            Consumption.read_xml_element(self, xml)

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self, errors):
        """
        Validates this consumption against rules which are not imposed by XSD.

        :param list errors: A list of error messages.
        """
        resource = self._node.get_resource_by_name(self._resource_name)
        if not resource:
            err = {'uri': self.get_uri(),
                   'rule': 'A consumption requires a resource.',
                   'error': "Resource '{0!s}' not found.".format(self._resource_name)}
            errors.append(err)
            return

        resource_type = resource.get_type()
        if not resource_type == 'CountingResource':
            # resource is not a valid resource for this consumption.
            err = {'uri': self.get_uri(),
                   'rule': 'A consumption requires a corresponding resource type.',
                   'error': "Found a resource of type '{0!s}', expecting a resource of type 'CountingResource'.".format(resource_type)}
            errors.append(err)

    # ------------------------------------------------------------------------------------------------------------------
    def store(self, nod_id):
        """
        Stores the definition of this consumption into the database.

        :param int nod_id: The ID of the node to which this consumption belongs.
        """
        resource = self._node.get_resource_by_name(self._resource_name)
        rsc_id = resource.get_rsc_id()
        uri_id = DataLayer.enk_misc_insert_uri(self.get_uri())

        self._cns_id = DataLayer.enk_reader_consumption_store_counting_consumption(nod_id,
                                                                                   rsc_id,
                                                                                   uri_id,
                                                                                   self._amount)


# ----------------------------------------------------------------------------------------------------------------------
