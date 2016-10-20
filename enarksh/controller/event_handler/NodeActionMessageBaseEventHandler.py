"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import enarksh
from enarksh.controller.Schedule import Schedule


class NodeActionMessageBaseEventHandler:
    """
    A base event handler for a NodeActionMessage or received events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def base_handle(controller, response, sch_id, rnd_id, act_id):
        """
        Handles a NodeActionMessage received event.

        :param enarksh.controller.Controller.Controller controller: The controller.
        :param dict response: The response to the client.
        :param int sch_id: The ID of the schedule.
        :param int rnd_id: The ID of the node.
        :param int act_id: The ID of the requested action.
        """
        schedule = controller.get_schedule_by_sch_id(sch_id)
        if schedule:
            actions = schedule.request_possible_node_actions(rnd_id)
        else:
            actions = Schedule.get_response_template()

        if act_id not in actions['actions'] or not actions['actions'][act_id]['act_enabled']:
            response['ret'] = -1
            response['message'] = 'Not a valid action'
        else:
            schedule = controller.get_schedule_by_sch_id(sch_id)
            reload = schedule.request_node_action(rnd_id, act_id)
            if reload:
                # Schedule must be reloaded.
                schedule = controller.reload_schedule(schedule.sch_id)
                # A reload is only required when the schedule is been triggered. However, this trigger is lost by
                # reloading the schedule. So, resend the trigger.
                schedule.request_node_action(schedule.get_activate_node().rnd_id, act_id)

            if act_id == enarksh.ENK_ACT_ID_TRIGGER:
                response['new_run'] = 1

# ----------------------------------------------------------------------------------------------------------------------
