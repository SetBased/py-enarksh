"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from cleo import Command

from enarksh.controller.client.LoadHostClient import LoadHostClient
from enarksh.style.EnarkshStyle import EnarkshStyle


class LoadHostCommand(Command):
    """
    Requests the controller to load a host definition

    load_host
        {host.xml : The host definition to load}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the load host command.
        """
        self.output = EnarkshStyle(self.input, self.output)

        client = LoadHostClient()
        ret = client.main(self.input.get_argument('host.xml'))

        return ret

# ----------------------------------------------------------------------------------------------------------------------
