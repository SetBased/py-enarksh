"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import fcntl
import os
import signal

import zmq

from enarksh.event.Event import Event
from enarksh.message.Message import Message


class EventQueueEmptyEventHandler:
    """
    An event handler for an empty event queue.
    """
    __wake_up_pipe = None
    """
    The wakeup file descriptor when a signal is received.

    :type: None|(int,int)
    """

    # ------------------------------------------------------------------------------------------------------------------
    @classmethod
    def init(cls):
        """
        Creates a pipe for waking up a select call when a signal has been received.
        """
        cls.__wake_up_pipe = os.pipe()
        fcntl.fcntl(cls.__wake_up_pipe[0], fcntl.F_SETFL, os.O_NONBLOCK)

        signal.set_wakeup_fd(EventQueueEmptyEventHandler.__wake_up_pipe[1])

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, _event_data, spawner):
        """
        Handles an empty event queue event.

        :param  _event: The event.
        :param * _event_data: Not used.
        :param enarksh.spawner.Spawner.Spawner spawner: The spawner.
        """
        del _event, _event_data

        # List with all file descriptors for reading.
        # Add the file descriptor for waking up select when a signal has been received.
        read = [EventQueueEmptyEventHandler.__wake_up_pipe[0]]

        # Add the sockets for incoming messages to the list of read file descriptors.
        zmq_fds = set()
        for socket in Message.message_controller.end_points.values():
            if socket.type in [zmq.PULL, zmq.REP]:
                read.append(socket)
                zmq_fds.add(socket)

        # Add the job handlers to the list of read file descriptors.
        for job_handler in spawner.job_handlers.values():
            fd_stdout = job_handler.stdout
            if fd_stdout >= 0:
                read.append(fd_stdout)
            fd_stderr = job_handler.stderr
            if fd_stderr >= 0:
                read.append(fd_stderr)

        # Unblock interrupts.
        signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGCHLD, signal.SIGHUP})

        try:
            # Wait for a fd becomes available for read or wait for an interrupt.
            read, _, except_fds = zmq.sugar.poll.select(read, [], [])
            # Somehow the sockets of the job handlers end up in the list of sockets with exceptions?!
            read = read + except_fds

        except InterruptedError:
            # Ignore Interrupted system call errors (EINTR) in the select call.
            # Note: In Python 3.5 EINTR will not occur any more. Nevertheless, we must only allow interrupts here to
            # prevent unwanted side effect of the signal handlers.
            read = []

        # Block all interrupts to prevent interrupted system call errors (EINTR).
        signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGCHLD, signal.SIGHUP})

        zmq_event = False
        for fd in read:
            if fd in zmq_fds:
                # fd of the message queue is ready to receive data.
                zmq_event = True
            elif fd == EventQueueEmptyEventHandler.__wake_up_pipe[0]:
                os.read(EventQueueEmptyEventHandler.__wake_up_pipe[0], 512)
            else:
                # fd of one or more job handlers are ready to receive data.
                for job_handler in spawner.job_handlers.values():
                    if fd == job_handler.stdout:
                        job_handler.read(fd)
                    if fd == job_handler.stderr:
                        job_handler.read(fd)

        if zmq_event:
            spawner.zmq_incoming_message_event.fire()
        else:
            Event.event_controller.event_queue_empty.fire()  # XXX test queue is empty

# ----------------------------------------------------------------------------------------------------------------------
