"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.DataLayer import DataLayer
from enarksh.xml_reader.Host import Host
from enarksh.xml_reader.node.ComplexNode import ComplexNode


class ScheduleNode(ComplexNode):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent_node):
        ComplexNode.__init__(self, parent_node)

        self._host = Host()
        self._host.load_db('localhost')

    # ------------------------------------------------------------------------------------------------------------------
    def get_resource_by_name(self, resource_name):
        """
        Returns a resource of this node.

        :param str resource_name: The name of the resource.

        :rtype: Resource
        """
        resource = ComplexNode.get_resource_by_name(self, resource_name)

        if not resource:
            resource = self._host.get_resource_by_name(resource_name)

        return resource

    # ------------------------------------------------------------------------------------------------------------------
    def store(self, srv_id, p_nod_master):
        """
        Stores the definition of this node into the database.

        :param int srv_id: The ID of the schedule revision to which this node belongs.
        :param int p_nod_master:
        """
        ComplexNode.store(self, srv_id, p_nod_master)

        self.store_dependencies()

        nod_id_activate = 0
        nod_id_arrest = 0
        for child_node in self._child_nodes.values():
            if child_node.is_activate_node():
                nod_id_activate = child_node.nod_id
            if child_node.is_arrest_node():
                nod_id_arrest = child_node.nod_id

        DataLayer.enk_reader_node_store_schedule_addendum(srv_id,
                                                          nod_id_activate,
                                                          nod_id_arrest,
                                                          self._nod_id)

    # ------------------------------------------------------------------------------------------------------------------
    def _store_self(self, srv_id, uri_id, p_nod_master):
        """
        Stores the definition of this node into the database.

        :param int srv_id: The ID of the schedule to which this node belongs.
        :param int uri_id: The ID of the URI of this node.
        :param int p_nod_master:
        """
        self._nod_id = DataLayer.enk_reader_node_store_schedule(srv_id,
                                                                uri_id,
                                                                self._node_name,
                                                                p_nod_master)

# ----------------------------------------------------------------------------------------------------------------------
