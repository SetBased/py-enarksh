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
from enarksh.controller.Controller import Controller
from enarksh.style.EnarkshStyle import EnarkshStyle


class ControllerCommand(Command):
    """
    Starts the controller

    controller
        {--d|daemonize : Become a daemon}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the controller command.
        """
        self.output = EnarkshStyle(self.input, self.output)

        controller = Controller()

        if self.option('daemonize'):
            output = open(os.path.join(enarksh.HOME, 'var/log/controllerd.log'), 'ab', 0)

            context = DaemonContext()
            context.working_directory = enarksh.HOME
            context.umask = 0o002
            context.pidfile = PIDLockFile(os.path.join(enarksh.HOME, 'var/lock/controllerd.pid'), False)
            context.stdout = output
            context.stderr = output
            with context:
                controller.main()

        controller.main()

# ----------------------------------------------------------------------------------------------------------------------
