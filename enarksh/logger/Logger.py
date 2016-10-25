"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import logging
import os
import pwd
import zmq

import enarksh
from enarksh.DataLayer import DataLayer
from enarksh.event.EventController import EventController
from enarksh.logger.event_handler.ExitMessageEventHandler import ExitMessageEventHandler
from enarksh.logger.event_handler.LogFileMessageEventHandler import LogFileMessageEventHandler
from enarksh.logger.message.LogFileMessage import LogFileMessage
from enarksh.message.ExitMessage import ExitMessage
from enarksh.message.MessageController import MessageController


class Logger:
    """
    The logger.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        self.__event_controller = EventController()
        """
        The event controller.

        :type: enarksh.event.EventController.EventController
        """

        self.__message_controller = MessageController()
        """
        The message controller.

        :type: enarksh.message.MessageController.MessageController
        """

        self.__log = logging.getLogger('enarksh')
        """
        The logger.

        :type: logging.Logger
        """

    # ------------------------------------------------------------------------------------------------------------------
    def main(self):
        """
        The main of the logger.
        """
        # Startup logger.
        self.__startup()

        # Register our socket for asynchronous incoming messages.
        self.__message_controller.register_end_point('pull', zmq.PULL, enarksh.LOGGER_PULL_END_POINT)

        # Register supported message types
        self.__message_controller.register_message_type(ExitMessage.MESSAGE_TYPE)
        self.__message_controller.register_message_type(LogFileMessage.MESSAGE_TYPE)

        # Register message received event handlers.
        self.__message_controller.register_listener(ExitMessage.MESSAGE_TYPE, ExitMessageEventHandler.handle)
        self.__message_controller.register_listener(LogFileMessage.MESSAGE_TYPE, LogFileMessageEventHandler.handle)

        # Register other event handlers.
        self.__event_controller.event_queue_empty.register_listener(self.__message_controller.receive_message)

        # Run the event loop.
        self.__event_controller.loop()

        # Shutdown logger.
        self.__shutdown()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __set_unprivileged_user():
        """
        Set the real and effective user and group to an unprivileged user.
        """
        _, _, uid, gid, _, _, _ = pwd.getpwnam('enarksh')

        os.setresgid(gid, gid, 0)
        os.setresuid(uid, uid, 0)

    # ------------------------------------------------------------------------------------------------------------------
    def __shutdown(self):
        """
        Performs the necessary actions for stopping the logger.
        """
        self.__log.info('Stopping logger')

    # ------------------------------------------------------------------------------------------------------------------
    def __startup(self):
        """
        Performs the necessary actions for starting up the logger.
        """
        self.__log.info('Starting logger')

        # Set the effective user and group to an unprivileged user and group.
        self.__set_unprivileged_user()

        # Set database configuration options.
        DataLayer.config['host'] = enarksh.MYSQL_HOSTNAME
        DataLayer.config['user'] = enarksh.MYSQL_USERNAME
        DataLayer.config['password'] = enarksh.MYSQL_PASSWORD
        DataLayer.config['database'] = enarksh.MYSQL_SCHEMA
        DataLayer.config['port'] = enarksh.MYSQL_PORT

# ----------------------------------------------------------------------------------------------------------------------
