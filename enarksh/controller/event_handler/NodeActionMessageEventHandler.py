"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import logging

from enarksh.DataLayer import DataLayer
from enarksh.controller.event_handler.NodeActionMessageBaseEventHandler import NodeActionMessageBaseEventHandler


class NodeActionMessageEventHandler(NodeActionMessageBaseEventHandler):
    """
    An event handler for a NodeActionMessage received events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, message, controller):
        """
        Handles a NodeActionMessage received event.

        :param * _event: Not used.
        :param enarksh.controller.message.NodeActionMessage.NodeActionMessage message: The message.
        :param enarksh.controller.Controller.Controller controller: The controller.
        """
        del _event

        log = logging.getLogger('enarksh')

        # Compose a response message for client.
        response = {'ret':     0,
                    'message': 'OK'}

        try:
            run_node = DataLayer.enk_back_run_node_find_by_uri(message.uri)

            if run_node:
                NodeActionMessageBaseEventHandler.base_handle(controller,
                                                              response,
                                                              run_node['sch_id'],
                                                              run_node['rnd_id'],
                                                              message.act_id)
                response['ret'] = 0
                response['message'] = 'Node {} has been queued'.format(message.uri)

            else:
                response['ret'] = 1
                response['message'] = 'Node {} does not exists'.format(message.uri)

            DataLayer.commit()
        except Exception as exception:
            log.exception('Error')

            response['ret'] = -1
            response['message'] = str(exception)

            DataLayer.rollback()

        # Send response message to the CLI client.
        controller.message_controller.send_message('lockstep', response)

# ----------------------------------------------------------------------------------------------------------------------
