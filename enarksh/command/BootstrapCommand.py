"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import os

from cleo import Command

from enarksh.Bootsrap import Bootstrap
from enarksh.C import C
from enarksh.style.EnarkshStyle import EnarkshStyle


class BootstrapCommand(Command):
    """
    Executes bootstrap

    bootstrap
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the bootstrap command.
        """
        self.output = EnarkshStyle(self.input, self.output)

        os.chdir(C.HOME)

        bootstrap = Bootstrap()
        bootstrap.main()

# ----------------------------------------------------------------------------------------------------------------------
