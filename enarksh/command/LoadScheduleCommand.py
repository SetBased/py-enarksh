"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
# ----------------------------------------------------------------------------------------------------------------------
from cleo import Command

from enarksh.util.LoadSchedule import LoadSchedule
from enarksh.style.EnarkshStyle import EnarkshStyle


# ----------------------------------------------------------------------------------------------------------------------
class LoadScheduleCommand(Command):
    """
    Loads the schedule.
    """

    name = 'load_schedule'

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the load schedule command.
        """
        self.output = EnarkshStyle(self.input, self.output)

        reader = LoadSchedule()
        reader.main()

# ----------------------------------------------------------------------------------------------------------------------
