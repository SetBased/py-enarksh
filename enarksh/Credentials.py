"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from configparser import ConfigParser

from enarksh.C import C


class Credentials:
    """
    Singleton for reading MySQL's credentials.
    """
    instance = None
    """
    The singleton of this class.

    :type: None|enarksh.Credentials.Credentials
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get():
        """
        Returns the singleton of this class.

        :rtype: enarksh.Credentials.Credentials
        """
        if not Credentials.instance:
            Credentials.instance = Credentials()

        return Credentials.instance

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        self.__config = ConfigParser()
        self.__config.read(C.CREDENTIALS_CFG)

    # ------------------------------------------------------------------------------------------------------------------
    def get_host(self):
        """
        Returns the hostname of the MySQL instance.

        :rtype: str
        """
        return self.__config.get('database', 'host', fallback='localhost')

    # ------------------------------------------------------------------------------------------------------------------
    def get_user(self):
        """
        Returns the user for connecting to the MySQL instance.

        :rtype: str
        """
        return self.__config.get('database', 'user')

    # ------------------------------------------------------------------------------------------------------------------
    def get_password(self):
        """
        Returns the password for connecting to the MySQL instance.

        :rtype: str
        """
        return self.__config.get('database', 'password')

    # ------------------------------------------------------------------------------------------------------------------
    def get_database(self):
        """
        Returns the database or schema name.

        :rtype: str
        """
        return self.__config.get('database', 'database')

    # ------------------------------------------------------------------------------------------------------------------
    def get_port(self):
        """
        Returns the port to the MySQL instance.

        :rtype: int
        """
        return self.__config.getint('database', 'port', fallback=3306)

# ----------------------------------------------------------------------------------------------------------------------
