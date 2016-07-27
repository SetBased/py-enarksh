"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from lxml import etree

import enarksh
from enarksh.XmlReader.Host import Host
from enarksh.XmlReader.Node import create_node, ScheduleNode, CompoundJobNode


class XmlReader:
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def parse_schedule(xml: str, filename: str) -> ScheduleNode:
        """
        Parses a schedule definition in XML.
        :param xml: The XML with a schedule definition
        """
        with open(enarksh.HOME + '/etc/enarksh.xsd', 'rb') as f:
            xsd = f.read()

        etree.clear_error_log()
        schema_root = etree.XML(xsd)
        schema = etree.XMLSchema(schema_root)
        parser = etree.XMLParser(schema=schema, encoding='utf8')
        try:
            root = etree.fromstring(bytes(xml, 'utf8'), parser)

            # Root element must be a schedule.
            if root.tag != 'Schedule':
                raise Exception("Root element must be 'Schedule' but '%s' was found." % root.tag)

            schedule = create_node('Schedule')
            schedule.read_xml(root)
            error = schedule.validate()
            if error:
                raise Exception("File '%s' is not a valid schedule configuration file.\n%s" % (filename, error))

            # Set recursion and dependency levels.
            schedule.set_levels()
        except etree.XMLSyntaxError as exception:
            print(exception.error_log.filter_from_level(etree.ErrorLevels.WARNING))
            raise exception

        return schedule

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def parse_dynamic_worker(xml: str, parent) -> CompoundJobNode:
        """
        Parses a schedule definition in XML.
        :param xml: The XML with a schedule definition
        """
        with open(enarksh.HOME + '/etc/enarksh.xsd', 'rb') as f:
            xsd = f.read()

        schema_root = etree.XML(xsd)
        schema = etree.XMLSchema(schema_root)
        parser = etree.XMLParser(schema=schema, encoding='utf8')
        root = etree.fromstring(bytes(xml, 'utf8'), parser)

        # Root element must be a dynamic inner worker.
        if root.tag != 'DynamicInnerWorker':
            raise Exception("Root element must be 'DynamicInnerWorker' but '%s' was found." % root.tag)

        worker = create_node('DynamicInnerWorker')
        worker.read_xml(root)
        error = worker.validate(parent)
        if error:
            raise Exception("XML message is not a valid dynamic worker configuration.\n%s" % error)

        # Set recursion and dependency levels.
        worker.set_levels()

        return worker

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def parse_host(filename: str) -> Host:
        """
        Parses a host definition in XML.
        :param filename: The XML file with a host definition
        :return: Host
        """
        with open(filename, 'rt', encoding='utf-8') as f:
            xml = f.read()

        with open(enarksh.HOME + '/etc/enarksh.xsd', 'rb') as f:
            xsd = f.read()

        schema_root = etree.XML(xsd)
        schema = etree.XMLSchema(schema_root)
        parser = etree.XMLParser(schema=schema, encoding='utf8')
        root = etree.fromstring(bytes(xml, 'utf8'), parser)

        # Root element must be a schedule.
        if root.tag != 'Host':
            raise Exception("Root element must be 'Host' but '%s' was found." % root.tag)

        host = Host()
        host.read_xml(root)
        error = host.validate()
        if error:
            raise Exception("File '%s' is not a valid host configuration file.\n%s" % (filename, error))

        return host


# ----------------------------------------------------------------------------------------------------------------------
