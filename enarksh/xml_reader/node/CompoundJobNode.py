"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.DataLayer import DataLayer
from enarksh.xml_reader.node.ComplexNode import ComplexNode


class CompoundJobNode(ComplexNode):
    # ------------------------------------------------------------------------------------------------------------------
    def _store_self(self, srv_id, uri_id, p_nod_master):
        """
        Stores the definition of this node into the database.

        :param int srv_id: The ID of the schedule to which this node belongs.
        :param int uri_id: The ID of the URI of this node.
        :param int p_nod_master:
        """
        self._nod_id = DataLayer.enk_reader_node_store_compound_job(srv_id,
                                                                    uri_id,
                                                                    self._parent_node._nod_id,
                                                                    self._node_name,
                                                                    self._recursion_level,
                                                                    self._dependency_level,
                                                                    p_nod_master)

# ----------------------------------------------------------------------------------------------------------------------
