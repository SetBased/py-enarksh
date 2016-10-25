"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import logging

import enarksh
from enarksh.DataLayer import DataLayer
from enarksh.controller.event_handler.NodeActionMessageBaseEventHandler import NodeActionMessageBaseEventHandler


class NagiosMessageEventHandler(NodeActionMessageBaseEventHandler):
    """
    An event handler for a NagiosMessage received events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, _message, controller):
        """
        Handles a NagiosMessage received event.

        :param * _event: Not used.
        :param * _message: Not used.
        :param enarksh.controller.Controller.Controller controller: The controller.
        """
        del _event, _message

        log = logging.getLogger('enarksh')

        rst_count = {enarksh.ENK_RST_ID_COMPLETED: 0,
                     enarksh.ENK_RST_ID_ERROR:     0,
                     enarksh.ENK_RST_ID_QUEUED:    0,
                     enarksh.ENK_RST_ID_RUNNING:   0,
                     enarksh.ENK_RST_ID_WAITING:   0}

        response = {'ret':       0,
                    'rst_count': rst_count,
                    'sch_count': len(controller.schedules)}

        try:
            for schedule in controller.schedules.values():
                schedule.nagios_performance_data(rst_count)

        except Exception as exception:
            log.exception('Error')

            response['ret'] = -1
            response['message'] = str(exception)

            DataLayer.rollback()

        # Send response message to the CLI client.
        controller.message_controller.send_message('lockstep', response)

# ----------------------------------------------------------------------------------------------------------------------
