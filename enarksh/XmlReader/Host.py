"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from lxml.etree import Element
from enarksh.DataLayer import DataLayer
from enarksh.XmlReader.Resource import create_resource, ReadWriteLockResource, CountingResource


class Host:
    """
    Program for loading a host definition into the database.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._hostname = ''
        """
        The name of this host.
        :type str:
        """

        self._hst_id = 0
        """
        The ID of this host when it is stored in the databases.
        :type int:
        """

        self._resources = {}
        """
        The resources of this host.
        :type dict:
        """

    # ------------------------------------------------------------------------------------------------------------------
    def load_db(self, hostname: str) -> None:
        """
        Loads the definition of this host from the database.
        :param hostname: The name of the host that must be loaded.
        """
        self._hostname = hostname

        host = DataLayer.enk_reader_host_load_host(hostname)
        self._hst_id = host['hst_id']

        resources_data = DataLayer.enk_back_get_host_resources()
        for resource_data in resources_data:
            resource = create_resource(resource_data['rtp_id'], resource_data['rsc_id'], None)
            self._resources[resource.get_name()] = resource

    # ------------------------------------------------------------------------------------------------------------------
    def get_resource_by_name(self, resource_name):
        if resource_name in self._resources:
            return self._resources[resource_name]

        return None

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml(self, xml: Element) -> None:
        for element in list(xml):
            tag = element.tag
            if tag == 'Hostname':
                self._hostname = element.text

            elif tag == 'Resources':
                self._read_xml_resources(element)

            else:
                raise Exception("Unexpected tag '{0!s}'.".format(tag))

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self) -> str:
        """
        Validates this node against rules which are not imposed by XSD.
        """
        errors = []
        self._validate_helper(errors)

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_helper(self, errors: list) -> None:
        """
        Helper function for validation this node.
        :param errors: A list of error messages.
        """
        if self._hostname != 'localhost':
            err = {'uri': self.get_uri(),
                   'rule': 'Currently, only localhost is supported.',
                   'error': "Hostname must be 'localhost', found: '{0!s}'.".format(self._hostname)}
            errors.append(err)

    # ------------------------------------------------------------------------------------------------------------------
    def get_uri(self, obj_type: str='host') -> str:
        """
        Returns the URI of this host.
        :param obj_type: The entity type.
        """
        return '//' + obj_type + '/' + self._hostname

    # ------------------------------------------------------------------------------------------------------------------
    def store(self) -> None:
        """
        Stores the definition of this host into the database.
        """
        # Get uri_id for this host.
        uri_id = DataLayer.enk_misc_insert_uri(self.get_uri())

        # Store the definition of the host self.
        self._store_self(uri_id)

        # Store the resources of this host.
        for resource in self._resources.values():
            resource.store(self._hst_id, None)

    # ------------------------------------------------------------------------------------------------------------------
    def _store_self(self, uri_id: int) -> None:
        """
        Stores the definition of this host into the database.
        :param uri_id: The ID of the URI of this node.
        """
        details = DataLayer.enk_reader_host_load_host(self._hostname)
        self._hst_id = details['hst_id']

    # ------------------------------------------------------------------------------------------------------------------
    def _read_xml_resources(self, xml: Element) -> None:
        for element in list(xml):
            tag = element.tag
            if tag == 'CountingResource':
                resource = CountingResource(self)

            elif tag == 'ReadWriteLockResource':
                resource = ReadWriteLockResource(self)

            else:
                raise Exception("Unexpected tag '{0!s}'.".format(tag))

            resource.read_xml(element)
            name = resource.get_name()
            # Check for resources with duplicate names.
            if name in self._resources:
                raise Exception("Duplicate resource '{0!s}'.".format(name))

            self._resources[name] = resource


# ----------------------------------------------------------------------------------------------------------------------
