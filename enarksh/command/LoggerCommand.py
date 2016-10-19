"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import os

from cleo import Command
from daemon import DaemonContext
from lockfile.pidlockfile import PIDLockFile

import enarksh
from enarksh.logger.Logger import Logger
from enarksh.style.EnarkshStyle import EnarkshStyle


class LoggerCommand(Command):
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
        self.output = EnarkshStyle(self.input, self.output)

        logger = Logger()

        if self.option('daemonize'):
            output = open(os.path.join(enarksh.HOME, 'var/log/loggerd.log'), 'ab', 0)

            context = DaemonContext()
            context.working_directory = enarksh.HOME
            context.umask = 0o002
            context.pidfile = PIDLockFile(os.path.join(enarksh.HOME, 'var/lock/loggerd.pid'), False)
            context.stdout = output
            context.stderr = output
            with context:
                logger.main()
        else:
            logger.main()

# ----------------------------------------------------------------------------------------------------------------------
