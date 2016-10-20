"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""

import enarksh
from enarksh.DataLayer import DataLayer
from enarksh.xml_reader.XmlReader import XmlReader


class LoadHostClient:
    """
    A client for requesting the controller to load a host definition.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        DataLayer.config['host'] = enarksh.MYSQL_HOSTNAME
        DataLayer.config['user'] = enarksh.MYSQL_USERNAME
        DataLayer.config['password'] = enarksh.MYSQL_PASSWORD
        DataLayer.config['database'] = enarksh.MYSQL_SCHEMA
        DataLayer.config['port'] = enarksh.MYSQL_PORT
        DataLayer.config['autocommit'] = False

    # ------------------------------------------------------------------------------------------------------------------
    def main(self, filename):
        """
        The main function of load_schedule.

        :param str filename: The filename with the XML definition of the host.
        """

        try:
            DataLayer.connect()

            reader = XmlReader()
            host = reader.parse_host(filename)
            host.store()

            DataLayer.commit()
            DataLayer.disconnect()
        except Exception as exception:
            DataLayer.rollback()
            DataLayer.disconnect()

            raise exception

# ----------------------------------------------------------------------------------------------------------------------
