"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import os

import zmq
from cleo import Command

import enarksh
from enarksh.message.HaltMessage import HaltMessage
from enarksh.style.EnarkshStyle import EnarkshStyle


class HaltCommand(Command):
    """
    Halts a daemon of Enarksh

    halt

        {daemon : The Enarksh daemon to halt: controllerd, loggerd, or spanwerd}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        Command.__init__(self)

        self._zmq_context = None
        """
        The ZMQ context.

        :type: Context
        """

        self.__end_points = {'controllerd': enarksh.CONTROLLER_PULL_END_POINT,
                             'loggerd':     enarksh.LOGGER_PULL_END_POINT,
                             'spawnerd':    enarksh.SPAWNER_PULL_END_POINT}
        """
        The end points of the Enarksh daemons.

        :type: dict[string,string]
        """

    # ------------------------------------------------------------------------------------------------------------------

    def __zmq_init(self):
        """
        Initializes ZMQ.
        """
        self._zmq_context = zmq.Context()

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self):
        """
        Executes the halt command.
        """
        self.output = EnarkshStyle(self.input, self.output)

        os.chdir(enarksh.HOME)

        self.__zmq_init()

        daemon = self.input.get_argument('daemon')

        if daemon not in self.__end_points:
            self.output.error("Unknown daemon '{}'".format(daemon))
            return -1

        # Connect tot the daemon.
        zmq_daemon = self._zmq_context.socket(zmq.PUSH)
        zmq_daemon.connect(self.__end_points[daemon])

        # Send the halt message tot the daemon.
        message = HaltMessage()
        zmq_daemon.send_pyobj(message)

# ----------------------------------------------------------------------------------------------------------------------
