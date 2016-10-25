"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.command.DaemonCommand import DaemonCommand
from enarksh.logger.Logger import Logger


class LoggerCommand(DaemonCommand):
    """
    Starts the logger

    logger
        {--d|daemonize : Become a daemon}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the logger command.
        """
        logger = Logger()

        self.handle_daemon('loggerd', logger)

# ----------------------------------------------------------------------------------------------------------------------
