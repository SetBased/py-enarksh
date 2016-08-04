"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.DataLayer import DataLayer

from enarksh.xml_reader.resource.Resource import Resource


class CountingResource(Resource):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node):
        Resource.__init__(self, node)

        self._amount = 0
        """
        The available amount of this resource.

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
            Resource.read_xml_element(self, xml)

    # ------------------------------------------------------------------------------------------------------------------
    def get_type(self):
        """
        Returns the name of the type of this resource type.

        :rtype: str
        """
        return 'CountingResource'

    # ------------------------------------------------------------------------------------------------------------------
    def load_db(self, rsc_id):
        details = DataLayer.enk_reader_resource_load_resource(rsc_id)

        self._rsc_id = rsc_id
        self._resource_name = str(details['rsc_name'], 'utf8')  # @todo XXX DL issue
        self._amount = details['rsc_amount']

    # ------------------------------------------------------------------------------------------------------------------
    def store(self, hst_id, nod_id):
        """
        :param int hst_id:
        :param int nod_id:
        """
        uri_id = DataLayer.enk_misc_insert_uri(self.get_uri())

        self._rsc_id = DataLayer.enk_reader_resource_store_counting_resource(hst_id,
                                                                             nod_id,
                                                                             uri_id,
                                                                             self._resource_name,
                                                                             self._amount)

# ----------------------------------------------------------------------------------------------------------------------
