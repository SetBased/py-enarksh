"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.Credentials import Credentials
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
        credentials = Credentials.get()

        DataLayer.config['host'] = credentials.get_host()
        DataLayer.config['user'] = credentials.get_user()
        DataLayer.config['password'] = credentials.get_password()
        DataLayer.config['database'] = credentials.get_database()
        DataLayer.config['port'] = credentials.get_port()
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
