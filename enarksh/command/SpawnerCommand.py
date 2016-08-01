"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
# ----------------------------------------------------------------------------------------------------------------------
from cleo import Command

from enarksh.Spawner.Spawner import Spawner
from enarksh.style.EnarkshStyle import EnarkshStyle


# ----------------------------------------------------------------------------------------------------------------------
class SpawnerCommand(Command):
    """
    Starts the spawner.
    """

    name = 'spawner'

    options = [
        {
            'name': 'daemonize',
            'shortcut': 'd',
            'flag': True,
            'description': 'If set, use demonize'
        }
    ]

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the logger command.
        """
        self._io = EnarkshStyle(self.input, self.output)

        spawner = Spawner()

        if self.option('daemonize'):
            spawner._daemonize()

        spawner.main()


# ----------------------------------------------------------------------------------------------------------------------
