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
from enarksh.controller.message.ScheduleDefinitionMessage import ScheduleDefinitionMessage


class LoadScheduleClient:
    """
    A client for requesting the controller to load new schedules.
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
    def main(self, filenames):
        """
        The main function of load_schedule.

        :param list[str] filenames: The filenames of the schedules to be loaded.
        """
        # Initialize ZMQ.
        self._zmq_init()

        # Send XML files to the controller.
        status = 0
        for filename in filenames:
            try:
                err = self._load_schedule(filename)
                if err:
                    status = -1
            except Exception as exception:
                print(exception, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                status = -1

        return status

    # ------------------------------------------------------------------------------------------------------------------
    def _zmq_init(self):
        """
        Initializes ZMQ.
        """
        self._zmq_context = zmq.Context()

        # Create socket for communicating with the controller.
        self._zmq_controller = self._zmq_context.socket(zmq.REQ)
        self._zmq_controller.connect(enarksh.CONTROLLER_LOCKSTEP_END_POINT)

    # ------------------------------------------------------------------------------------------------------------------
    def _load_schedule(self, filename):
        """
        Sends a message to the controller to load a new schedule definition.

        :param str filename: The name of XML file with the schedule definition.

        :rtype bool: True on success. Otherwise False.
        """
        with open(filename, 'rt', encoding='utf-8') as f:
            xml = f.read()

        # Compose the message for the controller.
        message = ScheduleDefinitionMessage(xml, os.path.realpath(filename))

        # Send the message to the controller.
        self._zmq_controller.send_pyobj(message)

        # Await the response from the controller.
        response = self._zmq_controller.recv_json()

        if response['ret'] == 0:
            self._io.log_verbose(response['message'])
        else:
            self._io.error(response['message'])

        return response['ret'] == 0

# ----------------------------------------------------------------------------------------------------------------------
