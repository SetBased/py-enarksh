"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.DataLayer import DataLayer
from enarksh.XmlReader.Node.ComplexNode import ComplexNode


class DynamicOuterWorkerNode(ComplexNode):
    # ------------------------------------------------------------------------------------------------------------------
    def _store_self(self, srv_id: int, uri_id: int, p_nod_master: int) -> None:
        """
        Stores the definition of this node into the database.
        :param srv_id: The ID of the schedule to which this node belongs.
        :param uri_id: The ID of the URI of this node.
        """
        self._nod_id = DataLayer.enk_reader_node_store_dynamic_outer_worker(srv_id,
                                                                            uri_id,
                                                                            self._parent_node._nod_id,
                                                                            self._node_name,
                                                                            self._recursion_level,
                                                                            self._dependency_level,
                                                                            p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_helper(self, errors: list) -> None:
        """
        Helper function for validation this node.
        :param errors: A list of error messages.
        """
        ComplexNode._validate_helper(self, errors)

        # Validate worker node has one and only one input port.
        if len(self._input_ports) != 1:
            err = {'uri': self.get_uri(),
                   'rule': 'A worker node must have one and only one input port.',
                   'error': "Node has {0:d} input ports.'.".format(len(self._input_ports))}
            errors.append(err)

        # Validate worker node has one and only one output port.
        if len(self._output_ports) != 1:
            err = {'uri': self.get_uri(),
                   'rule': 'A worker node must have one and only one output port.',
                   'error': "Node has {0:d} output ports.'.".format(len(self._output_ports))}
            errors.append(err)


# ----------------------------------------------------------------------------------------------------------------------
