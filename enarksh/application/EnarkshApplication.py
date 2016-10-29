"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from cleo import Application

from enarksh.command.BootstrapCommand import BootstrapCommand
from enarksh.command.LoadHostCommand import LoadHostCommand
from enarksh.command.LoadScheduleCommand import LoadScheduleCommand
from enarksh.command.NagiosCommand import NagiosCommand
from enarksh.command.NodeActionCommand import NodeActionCommand


class EnarkshApplication(Application):
    """
    The Enarksh application.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor
        """
        Application.__init__(self, 'Enarksh', '0.9.0')

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
        self.add(NagiosCommand())
        self.add(NodeActionCommand())

        return commands

# ----------------------------------------------------------------------------------------------------------------------
