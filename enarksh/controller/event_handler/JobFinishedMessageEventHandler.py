"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""


class JobFinishedMessageEventHandler:
    """
    An event handler for a JobFinishedMessage received events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, message, controller):
        """
        Handles a JobFinishedMessage received event.

        :param * _event: Not used.
        :param enarksh.controller.message.JobFinishedMessage.JobFinishedMessage message: The message.
        :param enarksh.controller.Controller.Controller controller: The controller.
        """
        del _event

        schedule = controller.get_schedule_by_sch_id(message.sch_id)
        schedule.node_stop(message.rnd_id, message.exit_status)

# ----------------------------------------------------------------------------------------------------------------------
