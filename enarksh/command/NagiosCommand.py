"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from cleo import Command

from enarksh.controller.client.NagiosClient import NagiosClient
from enarksh.style.EnarkshStyle import EnarkshStyle


class NagiosCommand(Command):
    """
    Test whether Enarksh is running properly.

    nagios
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the Nagios command.
        """
        self.output = EnarkshStyle(self.input, self.output)

        client = NagiosClient(self.output)
        ret = client.main()

        return ret

# ----------------------------------------------------------------------------------------------------------------------
