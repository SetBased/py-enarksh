"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
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
        self._event_controller = EventController()
        """
        The event controller.

        :type: enarksh.event.EventController.EventController
        """

        self._message_controller = MessageController()
        """
        The message controller.

        :type: enarksh.message.MessageController.MessageController
        """

    # ------------------------------------------------------------------------------------------------------------------
    def main(self):
        """
        The main of the logger.
        """
        # Startup logger.
        self._startup()

        # Register our socket for asynchronous incoming messages.
        self._message_controller.register_end_point('pull', zmq.PULL, enarksh.LOGGER_PULL_END_POINT)

        # Register supported message types
        self._message_controller.register_message_type(ExitMessage.MESSAGE_TYPE)
        self._message_controller.register_message_type(LogFileMessage.MESSAGE_TYPE)

        # Register message received event handlers.
        self._message_controller.register_listener(ExitMessage.MESSAGE_TYPE, ExitMessageEventHandler.handle)
        self._message_controller.register_listener(LogFileMessage.MESSAGE_TYPE, LogFileMessageEventHandler.handle)

        # Register other event handlers.
        self._event_controller.event_queue_empty.register_listener(self._message_controller.receive_message)

        # Run the event loop.
        self._event_controller.loop()

        # Shutdown logger.
        self._shutdown()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _shutdown():
        """
        Performs the necessary actions for stopping the logger.
        """
        # Log stop of the logger.
        print('Stop logger')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _startup():
        """
        Performs the necessary actions for starting up the logger.
        """
        # Log the start of the logger.
        print('Start logger')

        # Set database configuration options.
        DataLayer.config['host'] = enarksh.MYSQL_HOSTNAME
        DataLayer.config['user'] = enarksh.MYSQL_USERNAME
        DataLayer.config['password'] = enarksh.MYSQL_PASSWORD
        DataLayer.config['database'] = enarksh.MYSQL_SCHEMA
        DataLayer.config['port'] = enarksh.MYSQL_PORT

# ----------------------------------------------------------------------------------------------------------------------
