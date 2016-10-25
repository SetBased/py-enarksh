"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import logging

from enarksh.DataLayer import DataLayer
from enarksh.controller.Schedule import Schedule


class PossibleNodeActionsWebMessageEventHandler:
    """
    An event handler for a PossibleNodeActionsWebMessage received events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, message, controller):
        """
        Handles a PossibleNodeActionsWebMessage received event.

        :param * _event: Not used.
        :param enarksh.controller.message.PossibleNodeActionsWebMessage.PossibleNodeActionsWebMessage message:
               The message.
        :param enarksh.controller.Controller.Controller controller: The controller.
        """
        del _event

        log = logging.getLogger('enarksh')

        try:
            schedule = controller.get_schedule_by_sch_id(message.sch_id)
            if schedule:
                response = schedule.request_possible_node_actions(message.rnd_id)
            else:
                response = Schedule.get_response_template()

            DataLayer.commit()
        except Exception:
            log.exception('Error')

            response = dict()
            response['ret'] = -1
            response['message'] = 'Internal error'

            DataLayer.rollback()

        # Send the message to the web interface.
        controller.message_controller.send_message('lockstep', response, True)

# ----------------------------------------------------------------------------------------------------------------------
