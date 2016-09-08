"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import json

from enarksh.DataLayer import DataLayer
from enarksh.xml_reader.node.SimpleNode import SimpleNode


class CommandJobNode(SimpleNode):
    """
    Class for reading command job nodes.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent_node):
        """
        Object constructor.

        :param enarksh.xml_reader.node.Node.Node parent_node: The parent node of this node.
        """
        SimpleNode.__init__(self, parent_node)

        self._args = []
        """
        The arguments of the command.

        :type: list[str]
        """

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml_arg(self, xml):
        """
        Read the arguments of the job from a XML element.

        :param lxml.etree.Element xml: The XMl element.
        """
        tag = xml.tag
        if tag == 'Arg':
            self._args.append(xml.text)

        else:
            raise Exception("Unexpected tag '{0!s}'.".format(tag))

    # ------------------------------------------------------------------------------------------------------------------
    def read_xml_element(self, xml):
        """
        Read the properties of this node from a XML element.

        :param lxml.etree.Element xml: The XMl element.
        """
        tag = xml.tag
        if tag == 'Path':
            self._args.insert(0, xml.text)

        elif tag == 'Args':
            for element in list(xml):
                self.read_xml_arg(element)

        else:
            SimpleNode.read_xml_element(self, xml)

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_helper(self, errors):
        """
        Validates this consumption against rules which are not imposed by XSD.

        :param list errors: A list of error messages.
        """
        SimpleNode._validate_helper(self, errors)

        user_name = self.get_user_name()
        if not user_name:
            err = {'uri':   self.get_uri(),
                   'rule':  'A command job requires a user name under which it must run.',
                   'error': 'User name is not set.'}
            errors.append(err)

    # ------------------------------------------------------------------------------------------------------------------
    def _store_self(self, srv_id, uri_id, p_nod_master):
        """
        Stores the definition of this node into the database.

        :param int srv_id: The ID of the schedule to which this node belongs.
        :param int uri_id: The ID of the URI of this node.
        :param int p_nod_master:
        """
        self._nod_id = DataLayer.enk_reader_node_store_command_job(srv_id,
                                                                   uri_id,
                                                                   self._parent_node._nod_id,
                                                                   self._node_name,
                                                                   self._recursion_level,
                                                                   self._dependency_level,
                                                                   self._user_name,
                                                                   json.dumps(self._args),
                                                                   p_nod_master)

# ----------------------------------------------------------------------------------------------------------------------
