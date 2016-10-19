"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from cleo import Command

from enarksh.style.EnarkshStyle import EnarkshStyle
from enarksh.util.LoadSchedule import LoadSchedule


class LoadScheduleCommand(Command):
    """
    Loads schedules

    load_schedule
        {schedule.xml?* : The schedule(s) to load}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the load schedule command.
        """
        self.output = EnarkshStyle(self.input, self.output)

        reader = LoadSchedule()
        ret = reader.main(self.input.get_argument('schedule.xml'))

        return ret

# ----------------------------------------------------------------------------------------------------------------------
