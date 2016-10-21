"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from cleo import Command

from enarksh.controller.client.LoadScheduleClient import LoadScheduleClient
from enarksh.style.EnarkshStyle import EnarkshStyle


class LoadScheduleCommand(Command):
    """
    Requests the controller to load schedule definitions

    load_schedule
        {schedule.xml?* : The schedule(s) to load}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the load schedule command.
        """
        self.output = EnarkshStyle(self.input, self.output)

        client = LoadScheduleClient(self.output)
        ret = client.main(self.input.get_argument('schedule.xml'))

        return ret

# ----------------------------------------------------------------------------------------------------------------------
