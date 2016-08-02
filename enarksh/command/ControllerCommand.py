"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
# ----------------------------------------------------------------------------------------------------------------------
from cleo import Command

from enarksh.controller.Controller import Controller
from enarksh.style.EnarkshStyle import EnarkshStyle


# ----------------------------------------------------------------------------------------------------------------------
class ControllerCommand(Command):
    """
    Starts the controller.
    """

    name = 'controller'

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
        Executes the controller command.
        """
        self.output = EnarkshStyle(self.input, self.output)

        controller = Controller()

        if self.option('daemonize'):
            controller.daemonize()

        controller.main()


# ----------------------------------------------------------------------------------------------------------------------
