"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import zmq

import enarksh
from enarksh.controller.message.NodeActionMessage import NodeActionMessage


class NodeActionClient:
    """
    A client for requesting the controller for a node action.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io):
        """
        Object constructor.

        :param enarksh.style.EnarkshStyle.EnarkshStyle io: The output decorator.
        """
        self._zmq_context = None
        """
        The ZMQ context.

        :type: Context
        """

        self._zmq_controller = None
        """
        The socket for communicating with the controller.

        :type: zmq.sugar.socket.Socket
        """

        self._io = io
        """
        The output decorator.

        :type: enarksh.style.EnarkshStyle.EnarkshStyle
        """

    # ------------------------------------------------------------------------------------------------------------------
    def main(self, uri, act_id):
        """
        The main function of node_action.

        :param str uri: The URI of the (trigger) node that must be triggered.
        :param int act_id: The ID of the requested action.
        """
        # Initialize ZMQ.
        self._zmq_init()

        # Compose the message for the controller.
        message = NodeActionMessage(uri, act_id)

        # Send the message to the controller.
        self._zmq_controller.send_pyobj(message)

        # Await the response from the controller.
        response = self._zmq_controller.recv_pyobj()

        if response['ret'] == 0:
            self._io.log_verbose(response['message'])
        else:
            self._io.error(response['message'])

        return response['ret']

    # ------------------------------------------------------------------------------------------------------------------
    def _zmq_init(self):
        """
        Initializes ZMQ.
        """
        self._zmq_context = zmq.Context()

        # Create socket for communicating with the controller.
        self._zmq_controller = self._zmq_context.socket(zmq.REQ)
        self._zmq_controller.connect(enarksh.CONTROLLER_LOCKSTEP_END_POINT)

# ----------------------------------------------------------------------------------------------------------------------
