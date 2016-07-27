"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.DataLayer import DataLayer
from enarksh.XmlReader.Port.Port import Port


class OutputPort(Port):
    # ------------------------------------------------------------------------------------------------------------------
    def get_uri(self, obj_type: str='output_port') -> str:
        """
        Returns the URI of this output port.
        :param obj_type: The entity type.
        """
        if self._node:
            uri = self._node.get_uri(obj_type)
        else:
            uri = '//' + obj_type

        return uri + '/' + self._port_name

    # ------------------------------------------------------------------------------------------------------------------
    def store(self, nod_id: int) -> None:
        """
        Stores the definition of this port into the database.
        :param nod_id: The ID of the node to which this node belongs
        """
        uri_id = DataLayer.enk_misc_insert_uri(self.get_uri())
        self._prt_id = DataLayer.enk_reader_port_store_output_port(nod_id,
                                                                   uri_id,
                                                                   self._port_name)

    # ------------------------------------------------------------------------------------------------------------------
    def store_dependencies(self) -> None:
        for dependency in self._dependencies:
            dependency.store(self, self._node)


# ----------------------------------------------------------------------------------------------------------------------
