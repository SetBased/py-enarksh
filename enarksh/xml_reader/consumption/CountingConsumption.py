"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.DataLayer import DataLayer

from enarksh.xml_reader.consumption.Consumption import Consumption


class CountingConsumption(Consumption):
    """
    Class reading counting consumptions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node):
        """
        Object constructor.

        :param enarksh.xml_reader.node.Node.Node node: The node to which this consumption belongs.
        """
        Consumption.__init__(self, node)

        self._amount = 0
        """
        The amount that will be consumpted.

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml_element(self, xml):
        """
        Read the properties of this consumption from a XML element.

        :param lxml.etree.Element xml: The XMl element.
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
            err = {'uri':   self.get_uri(),
                   'rule':  'A consumption requires a resource.',
                   'error': "Resource '{0!s}' not found.".format(self._resource_name)}
            errors.append(err)
            return

        resource_type = resource.get_type()
        if not resource_type == 'CountingResource':
            # resource is not a valid resource for this consumption.
            err = {'uri':   self.get_uri(),
                   'rule':  'A consumption requires a corresponding resource type.',
                   'error': "Found a resource of type '{0!s}', expecting a resource of type 'CountingResource'.".format(
                       resource_type)}
            errors.append(err)

    # ------------------------------------------------------------------------------------------------------------------
    def store(self, nod_id):
        """
        Stores the definition of this consumption into the database.

        :param int nod_id: The ID of the node to which this consumption belongs.
        """
        resource = self._node.get_resource_by_name(self._resource_name)
        rsc_id = resource.rsc_id
        uri_id = DataLayer.enk_misc_insert_uri(self.get_uri())

        self._cns_id = DataLayer.enk_reader_consumption_store_counting_consumption(nod_id,
                                                                                   rsc_id,
                                                                                   uri_id,
                                                                                   self._amount)

# ----------------------------------------------------------------------------------------------------------------------
