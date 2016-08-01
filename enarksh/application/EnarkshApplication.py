"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
# ----------------------------------------------------------------------------------------------------------------------
from cleo import Application

from enarksh.command.BootstrapCommand import BootstrapCommand
from enarksh.command.LoadHostCommand import LoadHostCommand
from enarksh.command.LoadScheduleCommand import LoadScheduleCommand


# ----------------------------------------------------------------------------------------------------------------------
class EnarkshApplication(Application):
    """
    The Enarksh application.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def get_default_commands(self):
        """
        Returns the default commands of this application.

        :rtype: list[cleo.Command]
        """
        commands = Application.get_default_commands(self)

        self.add(BootstrapCommand())
        self.add(LoadHostCommand())
        self.add(LoadScheduleCommand())

        return commands


# ----------------------------------------------------------------------------------------------------------------------
