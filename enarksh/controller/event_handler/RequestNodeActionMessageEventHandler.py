"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import sys
import traceback

import enarksh
from enarksh.DataLayer import DataLayer
from enarksh.controller.Schedule import Schedule


class RequestNodeActionMessageEventHandler:
    """
    An event handler for a RequestNodeActionMessage received events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, message, controller):
        """
        Handles a JobFinishedMessage received event.

        :param * _event: Not used.
        :param enarksh.controller.message.RequestNodeActionMessage.RequestNodeActionMessage message: The message.
        :param enarksh.controller.Controller.Controller controller: The controller.
        """
        del _event

        # Compose a response message for the web interface.
        response = {'ret':     0,
                    'new_run': 0,
                    'message': 'OK'}

        try:
            schedule = controller.get_schedule_by_sch_id(message.sch_id)
            if schedule:
                actions = schedule.request_possible_node_actions(message.rnd_id)
            else:
                actions = Schedule.get_response_template()

            if message.act_id not in actions['actions'] or not actions['actions'][message.act_id]['act_enabled']:
                response['ret'] = -1
                response['message'] = 'Not a valid action'
            else:
                schedule = controller.get_schedule_by_sch_id(message.sch_id)
                reload = schedule.request_node_action(message.rnd_id,
                                                      message.act_id,
                                                      message.usr_login,
                                                      message.mail_on_completion,
                                                      message.mail_on_error)
                if reload:
                    # Schedule must be reloaded.
                    schedule = controller.reload_schedule(schedule.sch_id)
                    # A reload is only required when the schedule is been triggered. However, this trigger is lost by
                    # reloading the schedule. So, resend the trigger.
                    schedule.request_node_action(schedule.get_activate_node().rnd_id,
                                                 message.act_id,
                                                 message.usr_login,
                                                 message.mail_on_completion,
                                                 message.mail_on_error)

                    if message.act_id == enarksh.ENK_ACT_ID_TRIGGER:
                        response['new_run'] = 1
        except Exception as exception:
            print(exception, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

            response['ret'] = -1
            response['message'] = 'Internal error'

            DataLayer.rollback()

        # Send the message to the web interface.
        controller.message_controller.send_message('lockstep', response, True)

# ----------------------------------------------------------------------------------------------------------------------
