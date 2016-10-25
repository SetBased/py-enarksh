"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.command.DaemonCommand import DaemonCommand
from enarksh.controller.Controller import Controller


class ControllerCommand(DaemonCommand):
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
        controller = Controller()

        self.handle_daemon('controllerd', controller)

# ----------------------------------------------------------------------------------------------------------------------
