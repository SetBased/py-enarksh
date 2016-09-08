"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import sys
import traceback

from enarksh.DataLayer import DataLayer
from enarksh.controller.Schedule import Schedule


class RequestPossibleNodeActionsMessageEventHandler:
    """
    An event handler for a RequestPossibleNodeActions received events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, message, controller):
        """
        Handles a RequestPossibleNodeActions received event.

        :param * _event: Not used.
        :param enarksh.controller.message.RequestPossibleNodeActionsMessage.RequestPossibleNodeActionsMessage message:
               The message.
        :param enarksh.controller.Controller.Controller controller: The controller.
        """
        del _event

        try:
            schedule = controller.get_schedule_by_sch_id(message.sch_id)
            if schedule:
                response = schedule.request_possible_node_actions(message.rnd_id)
            else:
                response = Schedule.get_response_template()
        except Exception as exception:
            print(exception, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

            response = dict()
            response['ret'] = -1
            response['message'] = 'Internal error'

            DataLayer.rollback()

        # Send the message to the web interface.
        controller.message_controller.send_message('lockstep', response, True)

# ----------------------------------------------------------------------------------------------------------------------
