"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from cleo import Application

from enarksh.command.SpawnerCommand import SpawnerCommand


class SpawnerApplication(Application):
    """
    The Enarksh spawner application.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor
        """
        Application.__init__(self, 'Enarksh-Spawner', '0.9.0')

    # ------------------------------------------------------------------------------------------------------------------
    def get_default_commands(self):
        """
        Returns the default commands of this application.

        :rtype: list[cleo.Command]
        """
        commands = Application.get_default_commands(self)

        self.add(SpawnerCommand())

        return commands

# ----------------------------------------------------------------------------------------------------------------------
