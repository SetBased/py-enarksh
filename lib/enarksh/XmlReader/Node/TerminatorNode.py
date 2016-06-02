from lib.enarksh.DataLayer import DataLayer
from lib.enarksh.XmlReader.Node.ArrestNode import ArrestNode


# ----------------------------------------------------------------------------------------------------------------------
class TerminatorNode(ArrestNode):
    # ------------------------------------------------------------------------------------------------------------------
    def _store_self(self, srv_id: int, uri_id: int, p_nod_master: int) -> None:
        """
        Stores the definition of this node into the database.
        :param srv_id: The ID of the schedule to which this node belongs.
        :param uri_id: The ID of the URI of this node.
        """
        self._nod_id = DataLayer.enk_reader_node_store_terminator(srv_id,
                                                                  uri_id,
                                                                  self._parent_node._nod_id,
                                                                  self._node_name,
                                                                  self._recursion_level,
                                                                  self._dependency_level,
                                                                  p_nod_master)

# ----------------------------------------------------------------------------------------------------------------------
