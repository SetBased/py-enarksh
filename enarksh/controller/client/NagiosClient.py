"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import os

import zmq

import enarksh
from enarksh.C import C
from enarksh.Config import Config
from enarksh.controller.message.NagiosMessage import NagiosMessage


class NagiosClient:
    """
    A client for Nagios.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io):
        """
        Object constructor.

        :param enarksh.style.EnarkshStyle.EnarkshStyle io: The output decorator.
        """
        self.__zmq_context = None
        """
        The ZMQ context.

        :type: Context
        """

        self.__zmq_controller = None
        """
        The socket for communicating with the controller.

        :type: zmq.sugar.socket.Socket
        """

        self._io = io
        """
        The output decorator.

        :type: enarksh.style.EnarkshStyle.EnarkshStyle
        """

        self.__state = ''
        """
        The state for Nagios.

        :type: str
        """

        self.__message = ''
        """
        The message for Nagios.

        :type: str
        """

        self.__performance_data = ''
        """
        The performance data for Nagios.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __get_pid(daemon):
        """
        Returns the PID of a daemon of Enarksh.

        :param str daemon: The name of the daemon.

        :rtype: str|None
        """
        try:
            config = Config.get()

            pid_file = os.path.join(C.HOME, config.get_enarksh_lock_dir(), daemon + '.pid')
            with open(pid_file) as handle:
                pid = handle.read(1000)

            return int(pid)

        except Exception:
            return None

    # ------------------------------------------------------------------------------------------------------------------
    def __test_daemon_is_running(self, daemon):
        """
        Test whether a daemon is running.

        :param str daemon: The name of the daemon.

        :rtype: bool
        """
        pid = self.__get_pid(daemon)

        if pid is None:
            return False

        try:
            proc_file = os.path.join('/proc', str(pid), 'comm')
            name = open(proc_file).read(1000).strip()

            return name == daemon

        except Exception:
            return False

    # ------------------------------------------------------------------------------------------------------------------
    def __test_daemons_are_running(self):
        """
        Tests all 3 daemons are running.
        """
        # Test controller is running
        for daemon in ['controller', 'logger', 'spawner']:
            if not self.__test_daemon_is_running(daemon):
                if self.__message:
                    self.__message += ' '
                self.__message = '{} is not running'.format(daemon)

        if self.__message:
            self.__message = 'Enarksh CRITICAL - ' + self.__message
            self.__state = 2
        else:
            self.__message = 'Enarksh OK - '
            self.__state = 0

    # ------------------------------------------------------------------------------------------------------------------
    def __get_performance_data(self):
        """
        Retrieves performance data from the controller.
        """
        # Compose the message for the controller.
        message = NagiosMessage()

        # Send the message to the controller.
        self.__zmq_controller.send_pyobj(message)

        # Await the response from the controller.
        response = self.__zmq_controller.recv_pyobj()

        self.__performance_data += 'schedules={}, waiting={}, queued={}, running={}, completed={}, error={}'. \
            format(response['sch_count'],
                   response['rst_count'][C.ENK_RST_ID_WAITING],
                   response['rst_count'][C.ENK_RST_ID_QUEUED],
                   response['rst_count'][C.ENK_RST_ID_RUNNING],
                   response['rst_count'][C.ENK_RST_ID_COMPLETED],
                   response['rst_count'][C.ENK_RST_ID_ERROR])

        self.__message += 'Schedules = {}, Waiting = {}, Queued = {}, Running = {}, Completed = {}, Error = {}'. \
            format(response['sch_count'],
                   response['rst_count'][C.ENK_RST_ID_WAITING],
                   response['rst_count'][C.ENK_RST_ID_QUEUED],
                   response['rst_count'][C.ENK_RST_ID_RUNNING],
                   response['rst_count'][C.ENK_RST_ID_COMPLETED],
                   response['rst_count'][C.ENK_RST_ID_ERROR])

    # ------------------------------------------------------------------------------------------------------------------
    def main(self):
        """
        The main function of Nagios.
        """
        # Initialize ZMQ.
        self.__zmq_init()

        self.__test_daemons_are_running()

        if self.__state == 0:
            self.__get_performance_data()

        print(self.__message + '|' + self.__performance_data)

        return self.__state

    # ------------------------------------------------------------------------------------------------------------------
    def __zmq_init(self):
        """
        Initializes ZMQ.
        """
        config = Config.get()

        self.__zmq_context = zmq.Context()

        # Create socket for communicating with the controller.
        self.__zmq_controller = self.__zmq_context.socket(zmq.REQ)
        self.__zmq_controller.connect(config.get_controller_lockstep_end_point())

# ----------------------------------------------------------------------------------------------------------------------
