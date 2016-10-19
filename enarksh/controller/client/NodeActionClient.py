"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import os
import sys
import traceback

import zmq

import enarksh
from enarksh.controller.message.NodeActionMessage import NodeActionMessage
from enarksh.controller.message.ScheduleDefinitionMessage import ScheduleDefinitionMessage


class NodeActionClient:
    """
    A client for requesting the controller for a node action.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
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
        message = NodeActionMessage(uri, act_id, False, False)

        # Send the message to the controller.
        self._zmq_controller.send_pyobj(message)

        # Await the response from the controller.
        response = self._zmq_controller.recv_pyobj()

        print(response['message'], end='')
        if response['message'] and response['message'][-1:] != '\n':
            print()

        print(response)

        return response['ret']

    # ------------------------------------------------------------------------------------------------------------------
    def _zmq_init(self):
        self._zmq_context = zmq.Context()

        # Create socket for communicating with the controller.
        self._zmq_controller = self._zmq_context.socket(zmq.REQ)
        self._zmq_controller.connect(enarksh.CONTROLLER_LOCKSTEP_END_POINT)


# ----------------------------------------------------------------------------------------------------------------------
