"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.DataLayer import DataLayer
from enarksh.XmlReader.Host import Host
from enarksh.XmlReader.Node.ComplexNode import ComplexNode


class ScheduleNode(ComplexNode):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent_node):
        ComplexNode.__init__(self, parent_node)

        self._host = Host()
        self._host.load_db('localhost')

    # ------------------------------------------------------------------------------------------------------------------
    def get_resource_by_name(self, resource_name: str):
        """
        Returns a resource of this node.
        :param resource_name: The name of the resource.
        :return:
        """
        resource = ComplexNode.get_resource_by_name(self, resource_name)

        if not resource:
            resource = self._host.get_resource_by_name(resource_name)

        return resource

    # ------------------------------------------------------------------------------------------------------------------
    def store(self, srv_id: int, p_nod_master: int) -> None:
        """
        Stores the definition of this node into the database.
        :param srv_id: The ID of the schedule revision to which this node belongs.
        """
        ComplexNode.store(self, srv_id, p_nod_master)

        self.store_dependencies()

        nod_id_activate = 0
        nod_id_arrest = 0
        for child_node in self._child_nodes.values():
            if child_node.is_activate_node():
                nod_id_activate = child_node.get_nod_id()
            if child_node.is_arrest_node():
                nod_id_arrest = child_node.get_nod_id()

        DataLayer.enk_reader_node_store_schedule_addendum(srv_id,
                                                          nod_id_activate,
                                                          nod_id_arrest,
                                                          self._nod_id)

    # ------------------------------------------------------------------------------------------------------------------
    def _store_self(self, srv_id: int, uri_id: int, p_nod_master: int) -> None:
        """
        Stores the definition of this node into the database.
        :param srv_id: The ID of the schedule to which this node belongs.
        :param uri_id: The ID of the URI of this node.
        """
        self._nod_id = DataLayer.enk_reader_node_store_schedule(srv_id,
                                                                uri_id,
                                                                self._node_name,
                                                                p_nod_master)

# ----------------------------------------------------------------------------------------------------------------------
