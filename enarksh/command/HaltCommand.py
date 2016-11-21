"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import os

import zmq
from cleo import Command

from enarksh.C import C
from enarksh.Config import Config
from enarksh.message.HaltMessage import HaltMessage
from enarksh.style.EnarkshStyle import EnarkshStyle


class HaltCommand(Command):
    """
    Halts a daemon of Enarksh

    halt

        {daemon : The Enarksh daemon to halt: controller, logger, or spanwerd}
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

        self.__end_points = {}
        """
        The end points of the Enarksh daemons.

        :type: dict[string,string]
        """

    # ------------------------------------------------------------------------------------------------------------------
    def __read_config(self):
        """
        Reads the pull end point of the controller, logger, and spawner.
        """
        config = Config.get()

        self.__end_points['controller'] = config.get_controller_pull_end_point()
        self.__end_points['logger'] = config.get_logger_pull_end_point()
        self.__end_points['spawner'] = config.get_spawner_pull_end_point()

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

        os.chdir(C.HOME)

        self.__read_config()
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
