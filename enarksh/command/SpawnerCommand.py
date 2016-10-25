"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.command.DaemonCommand import DaemonCommand
from enarksh.spawner.Spawner import Spawner


class SpawnerCommand(DaemonCommand):
    """
    Starts the spawner

    spawner
        {--d|daemonize : Become a daemon}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the logger command.
        """
        spawner = Spawner()

        self.handle_daemon('spawnerd', spawner)

# ----------------------------------------------------------------------------------------------------------------------
