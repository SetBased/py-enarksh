"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import logging

from enarksh.DataLayer import DataLayer
from enarksh.controller.event_handler.NodeActionMessageBaseEventHandler import NodeActionMessageBaseEventHandler


class NodeActionMessageWebEventHandler(NodeActionMessageBaseEventHandler):
    """
    An event handler for a NodeActionWebMessage received events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, message, controller):
        """
        Handles a NodeActionWebMessage received event.

        :param * _event: Not used.
        :param enarksh.controller.message.NodeActionWebMessage.NodeActionWebMessage message: The message.
        :param enarksh.controller.Controller.Controller controller: The controller.
        """
        del _event

        log = logging.getLogger('enarksh')

        # Compose a response message for the web interface.
        response = {'ret':     0,
                    'new_run': 0,
                    'message': 'OK'}

        try:
            NodeActionMessageBaseEventHandler.base_handle(controller,
                                                          response,
                                                          message.sch_id,
                                                          message.rnd_id,
                                                          message.act_id)

            DataLayer.commit()
        except Exception:
            log.exception('Error')

            response['ret'] = -1
            response['message'] = 'Internal error'

            DataLayer.rollback()

        # Send the message to the web interface.
        controller.message_controller.send_message('lockstep', response, True)

# ----------------------------------------------------------------------------------------------------------------------
