"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from lxml.etree import Element

import enarksh
from enarksh.DataLayer import DataLayer
from enarksh.XmlReader.Consumption.Consumption import Consumption


class ReadWriteLockConsumption(Consumption):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, node):
        Consumption.__init__(self, node)

        self.rws_id = 0
        """
        The lock type.
        :type int:
        """

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml_element(self, xml: Element) -> None:
        tag = xml.tag
        if tag == 'Mode':
            mode = xml.text
            if mode == 'read':
                self.rws_id = enarksh.ENK_RWS_ID_READ

            elif mode == 'write':
                self.rws_id = enarksh.ENK_RWS_ID_WRITE

            else:
                raise Exception("Unexpected mode '{0!s}'.".format(mode))

        else:
            Consumption.read_xml_element(self, xml)

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self, errors: list) -> None:
        """
        Validates this consumption against rules which are not imposed by XSD.
        :param errors: A list of error messages.
        """
        resource = self._node.get_resource_by_name(self._resource_name)
        if not resource:
            err = {'uri': self.get_uri(),
                   'rule': 'A consumption requires a resource.',
                   'error': "Resource '{0!s}' not found.".format(self._resource_name)}
            errors.append(err)
            return

        resource_type = resource.get_type()
        if not resource_type == 'ReadWriteLockResource':
            # resource is not a valid resource for this consumption.
            err = {'uri': self.get_uri(),
                   'rule': 'A consumption requires a corresponding resource type.',
                   'error': "Found a resource of type '{0!s}', expecting a resource of type 'ReadWriteLockResource'.".format(resource_type)}
            errors.append(err)

    # ------------------------------------------------------------------------------------------------------------------
    def store(self, nod_id: int) -> None:
        """
        Stores the definition of this consumption into the database.
        :param nod_id: The ID of the node to which this consumption belongs.
        """
        resource = self._node.get_resource_by_name(self._resource_name)
        rsc_id = resource.get_rsc_id()
        uri_id = DataLayer.enk_misc_insert_uri(self.get_uri())

        self._cns_id = DataLayer.enk_reader_consumption_store_read_write_lock_consumption(nod_id,
                                                                                          rsc_id,
                                                                                          self.rws_id,
                                                                                          uri_id)


# ----------------------------------------------------------------------------------------------------------------------
