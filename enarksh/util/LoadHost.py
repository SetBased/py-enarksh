"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import argparse
import traceback
import sys

import enarksh

from enarksh.DataLayer import DataLayer
from enarksh.xml_reader.XmlReader import XmlReader


class LoadHost:
    """
    A program for loading a host definition file into Enarksh.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        # Set database configuration options.
        DataLayer.config['host'] = enarksh.MYSQL_HOSTNAME
        DataLayer.config['user'] = enarksh.MYSQL_USERNAME
        DataLayer.config['password'] = enarksh.MYSQL_PASSWORD
        DataLayer.config['database'] = enarksh.MYSQL_SCHEMA
        DataLayer.config['port'] = enarksh.MYSQL_PORT
        DataLayer.config['autocommit'] = False

    # ------------------------------------------------------------------------------------------------------------------
    def main(self):
        """
        The main function of load_schedule.
        """
        # Parse the arguments.
        parser = argparse.ArgumentParser(description='Description')
        parser.add_argument(dest='filename',
                            metavar='filename',
                            action='append',
                            help="XML file with a host definition")

        args = parser.parse_args()

        # Send XML files to the controller.
        exit_status = 0
        try:
            # Connect to the MySQL.
            DataLayer.connect()

            err = self._load_host(args.filename[0])

            DataLayer.commit()
            DataLayer.disconnect()
            if err:
                exit_status = -1
        except Exception as exception1:
            try:
                DataLayer.rollback()
                DataLayer.disconnect()
            except Exception as exception2:
                    print(exception2, file=sys.stderr)
                    traceback.print_exc(file=sys.stderr)
            print(exception1, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            exit_status = -1

        exit(exit_status)

    # ------------------------------------------------------------------------------------------------------------------
    def _load_host(self, filename):
        """
        :param str filename:
        """
        reader = XmlReader()
        host = reader.parse_host(filename)
        host.store()

# ----------------------------------------------------------------------------------------------------------------------
