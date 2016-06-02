import os
import signal
import sys
import select
import pwd
import zmq
from lib import enarksh
from lib.enarksh import SPAWNER_PULL_END_POINT, CONTROLLER_PULL_END_POINT, LOGGER_PULL_END_POINT
from lib.enarksh.Spawner.JobHandler import JobHandler


# ----------------------------------------------------------------------------------------------------------------------
class Spawner:
    _instance = None

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        Spawner._instance = self

        self._child_flag = False
        self._zmq_context = None
        self._zmq_pull_socket = None
        self._zmq_controller = None
        self._zmq_logger = None

        self._job_handlers = {}

    # ------------------------------------------------------------------------------------------------------------------
    def _zmq_init(self):
        self._zmq_context = zmq.Context()

        # Create socket for asynchronous incoming messages.
        self._zmq_pull_socket = self._zmq_context.socket(zmq.PULL)
        self._zmq_pull_socket.bind(SPAWNER_PULL_END_POINT)

        # Create socket for sending asynchronous messages to the controller.
        self._zmq_controller = self._zmq_context.socket(zmq.PUSH)
        self._zmq_controller.connect(CONTROLLER_PULL_END_POINT)

        # Create socket for sending asynchronous messages to the logger.
        self._zmq_logger = self._zmq_context.socket(zmq.PUSH)
        self._zmq_logger.connect(LOGGER_PULL_END_POINT)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _daemonize():
        enarksh.daemonize(enarksh.HOME + '/var/lock/spawnerd.pid',
                          '/dev/null',
                          enarksh.HOME + '/var/log/spawnerd.log',
                          enarksh.HOME + '/var/log/spawnerd.log')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def sigchld_handler(signum, frame):
        """
        Static method for SIGCHLD. Set a flag that a child has exited.
        """
        Spawner._instance._child_flag = True

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def sighup_handler(signum, frame):
        """
        SIGHUP is send by the log rotate daemon. CLoses the current log file and create a new log file.
        """
        sys.stdout.flush()
        sys.stderr.flush()

        with open(enarksh.HOME + '/var/log/spawnerd.log', 'wb', 0) as f:
            os.dup2(f.fileno(), sys.stdout.fileno())

        with open(enarksh.HOME + '/var/log/spawnerd.log', 'wb', 0) as f:
            os.dup2(f.fileno(), sys.stderr.fileno())

    # ------------------------------------------------------------------------------------------------------------------
    def _install_signal_handlers(self):
        """
        Install signal handlers for SIGCHLD and SIGHUP.
        """
        # Install signal handler for child has exited.
        signal.signal(signal.SIGCHLD, self.sigchld_handler)

        # Install signal handler log rotate.
        signal.signal(signal.SIGHUP, self.sighup_handler)

        # Unfortunately, restart system calls doesnt work.
        # signal.siginterrupt(signal.SIGCHLD, False)
        # signal.siginterrupt(signal.SIGHUP, False)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _set_unprivileged_user():
        """
        Set the real and effective user and group to an unprivileged user.
        """
        _, _, uid, gid, _, _, _ = pwd.getpwnam('enarksh')

        os.setresgid(gid, gid, 0)
        os.setresuid(uid, uid, 0)

    # ------------------------------------------------------------------------------------------------------------------
    def _startup(self):
        """
        Performs the necessary actions for starting the spawner daemon.
        """
        # Set the effective user and group to an unprivileged user and group.
        self._set_unprivileged_user()

        # Become a daemon.
        # self.__daemonize()

        # Install signal handlers.
        self._install_signal_handlers()

        self._zmq_init()

        # Read all user names under which the controller is allowed to start jobs.
        JobHandler.read_allowed_users()

    # ------------------------------------------------------------------------------------------------------------------
    def _handle_child_exits(self):
        """
        Handles an exit of a child and ends a jon handler.
        """
        try:
            pid = -1
            while pid != 0:
                pid, status = os.waitpid(-1, os.WNOHANG + os.WUNTRACED + os.WCONTINUED)
                if pid != 0:
                    job_handler = self._job_handlers[pid]

                    # Send message to controller that a job has finished.
                    message = {'type': 'node_stop',
                               'sch_id': job_handler.get_sch_id(),
                               'rnd_id': job_handler.get_rnd_id(),
                               'exit_status': status}
                    self._zmq_controller.send_json(message)

                    # Inform the job handler the job has finished.
                    job_handler.set_job_has_finished()

        except OSError:
            # Ignore OSError. No more children to wait for.
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def _event_handler_start_node(self, sch_id, rnd_id, user_name, args):
        """
        Creates a new job handler and starts the job.
        :param sch_id: The ID of the schedule of the job.
        :param rnd_id: The ID of the job.
        :param user_name: The user under which the job must run.
        :param args: The arguments for the job.
        """
        job_handler = JobHandler(sch_id, rnd_id, user_name, args)
        job_handler.start_job()

        self._job_handlers[job_handler.get_pid()] = job_handler

    # ------------------------------------------------------------------------------------------------------------------
    def _read_message(self):
        """
        Reads a message from the controller.
        """
        try:
            while True:
                message = self._zmq_pull_socket.recv_json(zmq.NOBLOCK)

                if message['type'] == 'start_node':
                    self._event_handler_start_node(message['sch_id'],
                                                   message['rnd_id'],
                                                   message['user_name'],
                                                   message['args'])

                else:
                    raise IndexError("Unknown message type '%s'." % message['type'])

        except zmq.ZMQError as e:
            # Ignore ZMQError with EAGAIN. Otherwise, re-raise the error.
            if e.errno != zmq.EAGAIN:
                raise e

    # ------------------------------------------------------------------------------------------------------------------
    def main(self):
        """
        The main function of the job spawner.
        """
        # Perform the necessary actions for starting up the spawner.
        self._startup()

        while True:
            # List with all file descriptors for reading.
            read = []

            # Add the queue for incoming messages to the list of read file descriptors.
            zmq_fd = self._zmq_pull_socket.get(zmq.FD)
            read.append(zmq_fd)

            # Add the job handlers to the list of read file descriptors.
            remove = []
            for pid, job_handler in self._job_handlers.items():
                fd_stdout = job_handler.get_stdout()
                if fd_stdout >= 0:
                    read.append(fd_stdout)
                fd_stderr = job_handler.get_stderr()
                if fd_stderr >= 0:
                    read.append(fd_stderr)

                if fd_stdout == -1 and fd_stderr == -1 and job_handler.get_pid() == -1:
                    # The job handler has read all data from stdout and stderr from job and the child process has
                    # exited.
                    remove.append(pid)

            # Remove jobs that are finished.
            for pid in remove:
                job_handler = self._job_handlers[pid]

                # Tell the job handler we are done with the job.
                job_handler.end_job()

                # Send messages to logger daemon that the stdout and stderr of the job can be loaded into
                # the database.
                self._zmq_logger.send_json(job_handler.get_logger_message('out'))
                self._zmq_logger.send_json(job_handler.get_logger_message('err'))

                # Remove the job from the dictionary with jobs.
                del self._job_handlers[pid]

            # Unblock interrupts.
            signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGCHLD, signal.SIGHUP})

            try:
                # Wait for a fd becomes available for read or wait for an interrupt.
                read, _, _ = select.select(read, [], [])

            except InterruptedError:
                # Ignore Interrupted system call errors (EINTR) in the select call.
                pass

            # Block all interrupts to prevent interrupted system call errors (EINTR).
            signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGCHLD, signal.SIGHUP})

            for fd in read:
                if fd == zmq_fd:
                    # fd of the message queue is ready to receive data.
                    self._read_message()
                else:
                    # fd of one or more job handlers are ready to receive data.
                    for _, job_handler in self._job_handlers.items():
                        if fd == job_handler.get_stdout():
                            job_handler.read(fd)
                        if fd == job_handler.get_stderr():
                            job_handler.read(fd)

            if self._child_flag:
                # Process one or more exited child processes.
                self._handle_child_exits()


# ----------------------------------------------------------------------------------------------------------------------
