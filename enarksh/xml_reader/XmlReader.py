"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import logging
import os

from lxml import etree

import enarksh
from enarksh.xml_reader.Host import Host
from enarksh.xml_reader.node import create_node


class XmlReader:
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def parse_schedule(xml, filename):
        """
        Parses a schedule definition in XML.

        :param str xml: The XML with a schedule definition
        :param str filename:

        :rtype: enarksh.xml_reader.node.ScheduleNode
        """
        with open(os.path.join(enarksh.HOME, 'etc/enarksh.xsd'), 'rb') as f:
            xsd = f.read()

        etree.clear_error_log()
        schema_root = etree.XML(xsd)
        schema = etree.XMLSchema(schema_root)
        parser = etree.XMLParser(schema=schema, encoding='utf8')
        try:
            root = etree.fromstring(bytes(xml, 'utf8'), parser)

            # Root element must be a schedule.
            if root.tag != 'Schedule':
                raise Exception("Root element must be 'Schedule' but '{0!s}' was found.".format(root.tag))

            schedule = create_node('Schedule')
            schedule.read_xml(root)
            error = schedule.validate()
            if error:
                raise Exception(
                    "File '{0!s}' is not a valid schedule configuration file.\n{1!s}".format(filename, error))

            # Set recursion and dependency levels.
            schedule.set_levels()
        except etree.XMLSyntaxError as exception:
            log = logging.getLogger('enarksh')
            log.error(exception.error_log.filter_from_level(etree.ErrorLevels.WARNING))
            raise exception

        return schedule

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def parse_dynamic_worker(xml, parent):
        """
        Parses a schedule definition in XML.

        :param str xml: The XML with a schedule definition
        :param parent:

        :rtype: enarksh.xml_reader.node.CompoundJobNode
        """
        with open(os.path.join(enarksh.HOME, 'etc/enarksh.xsd'), 'rb') as f:
            xsd = f.read()

        schema_root = etree.XML(xsd)
        schema = etree.XMLSchema(schema_root)
        parser = etree.XMLParser(schema=schema, encoding='utf8')
        root = etree.fromstring(bytes(xml, 'utf8'), parser)

        # Root element must be a dynamic inner worker.
        if root.tag != 'DynamicInnerWorker':
            raise Exception("Root element must be 'DynamicInnerWorker' but '{0!s}' was found.".format(root.tag))

        worker = create_node('DynamicInnerWorker')
        worker.read_xml(root)
        error = worker.validate(parent)
        if error:
            raise Exception("XML message is not a valid dynamic worker configuration.\n{0!s}".format(error))

        # Set recursion and dependency levels.
        worker.set_levels()

        return worker

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def parse_host(filename):
        """
        Parses a host definition in XML.

        :param str filename: The XML file with a host definition

        :rtype: enarksh.xml_reader.Host.Host
        """
        with open(filename, 'rt', encoding='utf-8') as f:
            xml = f.read()

        with open(os.path.join(enarksh.HOME, 'etc/enarksh.xsd'), 'rb') as f:
            xsd = f.read()

        schema_root = etree.XML(xsd)
        schema = etree.XMLSchema(schema_root)
        parser = etree.XMLParser(schema=schema, encoding='utf8')
        root = etree.fromstring(bytes(xml, 'utf8'), parser)

        # Root element must be a schedule.
        if root.tag != 'Host':
            raise Exception("Root element must be 'Host' but '{0!s}' was found.".format(root.tag))

        host = Host()
        host.read_xml(root)
        error = host.validate()
        if error:
            raise Exception("File '{0!s}' is not a valid host configuration file.\n{1!s}".format(filename, error))

        return host

# ----------------------------------------------------------------------------------------------------------------------
