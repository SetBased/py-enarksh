"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from configparser import ConfigParser

from enarksh.C import C


class Config:
    """
    Singleton for reading configuration parameters
    """
    instance = None
    """
    The singleton of this class.

    :type: None|enarksh.Config.Config
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get():
        """
        Returns the singleton of this class.

        :rtype: enarksh.Config.Config
        """
        if not Config.instance:
            Config.instance = Config()

        return Config.instance

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        self.__config = ConfigParser()
        self.__config.read(C.ENARKSH_CFG)

    # ------------------------------------------------------------------------------------------------------------------
    def get_controller_email(self):
        """
        Returns the sender's email address of Enarksh.

        :rtype: str
        """
        return self.__config.get('controller', 'email')

    # ------------------------------------------------------------------------------------------------------------------
    def get_controller_lockstep_end_point(self):
        """
        Returns the lockstep end point of the controller.

        :rtype: str
        """
        return self.__config.get('controller', 'lockstep_end_point')

    # ------------------------------------------------------------------------------------------------------------------
    def get_controller_pull_end_point(self):
        """
        Returns the pull end point of the controller.

        :rtype: str
        """
        return self.__config.get('controller', 'pull_end_point')

    # ------------------------------------------------------------------------------------------------------------------
    def get_enarksh_lock_dir(self):
        """
        Returns the directory name for storing lock files.

        :rtype: str
        """
        return self.__config.get('enarksh', 'lock_dir')

    # ------------------------------------------------------------------------------------------------------------------
    def get_enarksh_log_dir(self):
        """
        Returns the directory name for storing log files.

        :rtype: str
        """
        return self.__config.get('enarksh', 'log_dir')

    # ------------------------------------------------------------------------------------------------------------------
    def get_enarksh_log_back(self):
        """
        Returns the number of rotated log files.

        :rtype: int
        """
        return self.__config.getint('enarksh', 'log_backup')

    # ------------------------------------------------------------------------------------------------------------------
    def get_enarksh_max_log_size(self):
        """
        Returns the maximum size of a log file.

        :rtype: int
        """
        return self.__config.getint('enarksh', 'max_log_size')

    # ------------------------------------------------------------------------------------------------------------------
    def get_logger_pull_end_point(self):
        """
        Returns the pull end point of the logger.

        :rtype: str
        """
        return self.__config.get('logger', 'pull_end_point')

    # ------------------------------------------------------------------------------------------------------------------
    def get_spawner_get_users(self):
        """
        Returns the user accounts under which the spawner is allowed to start processes.

        :rtype: list[str]
        """
        users = self.__config.get('spawner', 'users')
        if users:
            return users.split(' ')

        return []

    # ------------------------------------------------------------------------------------------------------------------
    def get_spawner_pull_end_point(self):
        """
        Returns the pull end point of the spawner.

        :rtype: str
        """
        return self.__config.get('spawner', 'pull_end_point')

# ----------------------------------------------------------------------------------------------------------------------
