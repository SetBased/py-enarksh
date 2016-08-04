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
from enarksh.spawner.Spawner import Spawner
from enarksh.style.EnarkshStyle import EnarkshStyle


class SpawnerCommand(Command):
    """
    Starts the spawner.
    """

    name = 'spawner'

    options = [
        {
            'name':        'daemonize',
            'shortcut':    'd',
            'flag':        True,
            'description': 'Become a daemon'
        }
    ]

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the logger command.
        """
        self.output = EnarkshStyle(self.input, self.output)

        spawner = Spawner()

        if self.option('daemonize'):
            output = open(os.path.join(enarksh.HOME, 'var/log/spawnerd.log'), 'ab', 0)

            context = DaemonContext()
            context.working_directory = enarksh.HOME
            context.umask = 0o002
            context.pidfile = PIDLockFile(os.path.join(enarksh.HOME, 'var/lock/spawnerd.pid'), False)
            context.stdout = output
            context.stderr = output
            with context:
                spawner.main()
        else:
            spawner.main()

# ----------------------------------------------------------------------------------------------------------------------
