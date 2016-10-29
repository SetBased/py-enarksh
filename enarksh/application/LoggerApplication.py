"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from cleo import Application

from enarksh.command.LoggerCommand import LoggerCommand


class LoggerApplication(Application):
    """
    The Enarksh logger application.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor
        """
        Application.__init__(self, 'Enarksh-Logger', '0.9.0')

    # ------------------------------------------------------------------------------------------------------------------
    def get_default_commands(self):
        """
        Returns the default commands of this application.

        :rtype: list[cleo.Command]
        """
        commands = Application.get_default_commands(self)

        self.add(LoggerCommand())

        return commands

# ----------------------------------------------------------------------------------------------------------------------
