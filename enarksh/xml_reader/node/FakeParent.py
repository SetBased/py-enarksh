"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""


class FakeParent:
    def __init__(self, schedule, host_resources, nod_id, rnd_id):
        """
        Object constructor.

        :param schedule:
        :param dict host_resources:
        :param nod_id:
        :param rnd_id:
        """
        self._schedule = schedule
        self._host_resources = host_resources
        self._nod_id = nod_id

        self._node = schedule.get_node(rnd_id)

    # ------------------------------------------------------------------------------------------------------------------
    def get_resource_by_name(self, name):
        """
        :param str name:

        :rtype: enarksh.xml_reader.resource.Resource.Resource
        """
        resource = self._node.fake_get_resource_by_name(name)
        if resource:
            return resource

        for resource in self._host_resources.values():
            if resource.get_name() == name:
                return resource

        return None

    # ------------------------------------------------------------------------------------------------------------------
    def get_uri(self, obj_type='node'):
        """
        :param str obj_type:

        :rtype: str
        """
        return self._node.get_uri(obj_type)

# ----------------------------------------------------------------------------------------------------------------------
