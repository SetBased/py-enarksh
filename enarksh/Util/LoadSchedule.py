"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import argparse
import os
import traceback
import sys

import zmq

import enarksh


class LoadSchedule:
    """
    A client to communicates with the controller for loading a new schedule.
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
    def main(self):
        """
        The main function of load_schedule.
        """
        # Parse the arguments.
        parser = argparse.ArgumentParser(description='Description')
        parser.add_argument(dest='file_names',
                            metavar='filename',
                            action='append',
                            nargs='*',
                            help="XML file with a schedule definition")

        args = parser.parse_args()

        # Initialize ZMQ.
        self._zmq_init()

        # Send XML files to the controller.
        exit_status = 0
        for filename in args.file_names:
            try:
                err = self._load_schedule(filename[0])
                if err:
                    exit_status = -1
            except Exception as exception:
                print(exception, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                exit_status = -1

        exit(exit_status)

    # ------------------------------------------------------------------------------------------------------------------
    def _zmq_init(self):
        self._zmq_context = zmq.Context()

        # Create socket for communicating with the controller.
        self._zmq_controller = self._zmq_context.socket(zmq.REQ)
        self._zmq_controller.connect(enarksh.CONTROLLER_LOCKSTEP_END_POINT)

    # ------------------------------------------------------------------------------------------------------------------
    def _load_schedule(self, filename: str) -> bool:
        """
        Sends a message to the controller to load a new schedule definition.
        :param filename: The name of XML file with the schedule definition.
        :return: True on success. Otherwise False.
        """
        with open(filename, 'rt', encoding='utf-8') as f:
            xml = f.read()

        # Compose the message for the controller.
        message = {'type': 'schedule_definition',
                   'filename': os.path.realpath(filename),
                   'xml': xml}

        # Send the message tot the controller.
        self._zmq_controller.send_json(message)

        # Await the response from the controller.
        response = self._zmq_controller.recv_json()

        print(response['message'], end='')
        if response['message'][-1:] != '\n':
            print()

        return response['ret'] == 0

# ----------------------------------------------------------------------------------------------------------------------
