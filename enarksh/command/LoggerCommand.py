"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
# ----------------------------------------------------------------------------------------------------------------------
from cleo import Command

from enarksh.Logger.Logger import Logger
from enarksh.style.EnarkshStyle import EnarkshStyle


# ----------------------------------------------------------------------------------------------------------------------
class LoggerCommand(Command):
    """
    Starts the logger.
    """

    name = 'logger'

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
        self.output = EnarkshStyle(self.input, self.output)

        logger = Logger()

        if self.option('daemonize'):
            pass  # @todo do stuff

        logger.main()


# ----------------------------------------------------------------------------------------------------------------------
