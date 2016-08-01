"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
# ----------------------------------------------------------------------------------------------------------------------
from cleo import Application

from enarksh.command.ControllerCommand import ControllerCommand


# ----------------------------------------------------------------------------------------------------------------------
class ControllerApplication(Application):
    """
    The Enarksh controller application.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def get_default_commands(self):
        """
        Returns the default commands of this application.

        :rtype: list[cleo.Command]
        """
        commands = Application.get_default_commands(self)

        self.add(ControllerCommand())

        return commands

# ----------------------------------------------------------------------------------------------------------------------
