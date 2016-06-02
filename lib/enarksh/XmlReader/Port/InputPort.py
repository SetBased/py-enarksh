from lib.enarksh.DataLayer import DataLayer
from lib.enarksh.XmlReader.Port.Port import Port


# ----------------------------------------------------------------------------------------------------------------------
class InputPort(Port):
    # ------------------------------------------------------------------------------------------------------------------
    def get_dependency_level(self) -> int:
        dependency_level = -1
        for dependency in self._dependencies:
            level = dependency.get_dependency_level()
            if level > dependency_level:
                dependency_level = level

        return dependency_level

    # ------------------------------------------------------------------------------------------------------------------
    def get_uri(self, obj_type: str='input_port') -> str:
        """
        Returns the URI of this input port.
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
        self._prt_id = DataLayer.enk_reader_port_store_input_port(nod_id,
                                                                  uri_id,
                                                                  self._port_name)

    # ------------------------------------------------------------------------------------------------------------------
    def store_dependencies(self) -> None:
        for dependency in self._dependencies:
            dependency.store(self, self._node.get_parent_node())

# ----------------------------------------------------------------------------------------------------------------------
