"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import logging
import os
import pwd
import sys
from configparser import ConfigParser

import enarksh
from enarksh.event.Event import Event
from enarksh.event.EventActor import EventActor
from enarksh.logger.message.LogFileMessage import LogFileMessage
from enarksh.spawner.ChunkLogger import ChunkLogger


class JobHandler(EventActor):
    """
    Class for reading the stdout and stderr and monitoring the processes of a job.
    """
    __allowed_users = []
    """
    The list of user names under which a process can be started.

    :type: list[str]
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, sch_id, rnd_id, user_name, args):
        """
        Creates a job handler for starting a job.

        :param int sch_id: The ID of the schedule of the job.
        :param int rnd_id: The ID of the job.
        :param str user_name: The user under which the job must run.
        :param args: The arguments for the job.
        """
        EventActor.__init__(self)

        self.__sch_id = sch_id
        """
        The ID of the schedule of the job.

        :type: int
        """

        self.__rnd_id = rnd_id
        """
        The ID of the job.

        :type: int
        """

        self.__user_name = user_name
        """
        The user under which the job must run.

        :type: str
        """

        self.__args = args
        """
        The arguments for the job.

        :type: list[str]
        """

        self.stdout_logger = ChunkLogger()
        """
        The chunk logger for STDOUT of the job.

        :type: enarksh.spawner.ChunkLogger.ChunkLogger
        """

        self.stderr_logger = ChunkLogger()
        """
        The chunk logger for STDERR of the job.

        :type: enarksh.spawner.ChunkLogger.ChunkLogger
        """

        self.__child_pid = -1
        """
        The PID of the child process.

        :type: int
        """

        self.__stdout = -1
        """
        The fd for reading the STDOUT of the child process.

        :type: int
        """

        self.__stderr = -1
        """
        The fd for reading the STDERR of the child process.

        :type: int
        """

        self.final_event = Event(self)
        """
        The event that will be fired when the job has been finally done.

        :type: enarksh.event.Event.Event
        """

        self.__log = logging.getLogger('enarksh')
        """
        The logger.

        :type: logging.Logger
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def pid(self):
        """
        Returns the PID of the job. If the job is finished the pid is -1.

        :rtype int: The PID of the job.
        """
        return self.__child_pid

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def stderr(self):
        """
        Returns the file descriptor for reading the stderr of the child process.

        :rtype int: file descriptor
        """
        return self.__stderr

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def stdout(self):
        """
        Returns the file descriptor for reading the stdout of the child process.

        :rtype int: file descriptor
        """
        return self.__stdout

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def rnd_id(self):
        """
        Returns the ID of the job.

        :rtype: int
        """
        return self.__rnd_id

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def sch_id(self):
        """
        Returns the ID of the schedule of the job.

        :rtype: int
        """
        return self.__sch_id

    # ------------------------------------------------------------------------------------------------------------------
    def __log_job_start(self):
        """
        Logs the starting of a job.
        """
        self.__log.info('Start rnd_id: {0:10d}, {1:8s}, {2:s}'.
                        format(self.__rnd_id, self.__user_name, str(self.__args)))

    # ------------------------------------------------------------------------------------------------------------------
    def __log_job_stop(self):
        """
        Logs the end of job.
        """
        self.__log.info('End   rnd_id: {0:10d}'.format(self.__rnd_id))

    # ------------------------------------------------------------------------------------------------------------------
    def __final(self):
        """
        When the job is finally done fires a done event.
        """
        if self.__child_pid == -1 and self.__stdout == -1 and self.__stderr == -1:
            self.__log_job_stop()

            # Close the files of the chunk loggers.
            self.stdout_logger.close()
            self.stderr_logger.close()

            # Send messages to logger daemon that the stdout and stderr of the job can be loaded into the database.
            self.get_logger_message('out').send_message('logger')
            self.get_logger_message('err').send_message('logger')

            # Fire the event that this job has been done completely.
            self.final_event.fire()

    # ------------------------------------------------------------------------------------------------------------------
    def set_job_has_finished(self):
        """
        Marks that the job has finished.
        """
        self.__child_pid = -1
        self.__final()

    # ------------------------------------------------------------------------------------------------------------------
    def get_logger_message(self, std):
        """
        Returns a message for the logger.

        :param str std: log for stdout, err for stderr

        :rtype: enarksh.message.logger.LogFileMessage.LogFileMessage
        """
        if std == 'out':
            chunk_logger = self.stdout_logger
        elif std == 'err':
            chunk_logger = self.stderr_logger
        else:
            raise ValueError("Unknown output '%s'." % std)

        return LogFileMessage(self.__rnd_id,
                              std,
                              chunk_logger.get_total_log_size(),
                              chunk_logger.filename1,
                              chunk_logger.filename2)

    # ------------------------------------------------------------------------------------------------------------------
    def read(self, fd):
        """
        Reads data from the file descriptor and stores the data in a chunk logger.

        :param int fd: The file descriptor.
        """
        if fd == self.__stdout:
            data = os.read(fd, 1000)
            if data == b'':
                # The pipe has been closed by the child process.
                os.close(self.__stdout)
                self.__stdout = -1
                self.__final()
            else:
                self.stdout_logger.write(data)

        elif fd == self.__stderr:
            data = os.read(fd, 1000)
            if data == b'':
                # The pipe has been closed by the child process.
                os.close(self.__stderr)
                self.__stderr = -1
                self.__final()
            else:
                self.stdout_logger.write(data)
                self.stderr_logger.write(data)

        else:
            raise ValueError('Unknown file descriptor %d.' % fd)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def read_allowed_users():
        """
        Reads the user names under which enarksh is allowed to start processes.
        """
        config = ConfigParser()
        config.read(os.path.join(enarksh.HOME, 'etc/enarksh.cfg'))

        JobHandler.__allowed_users = config.get('spawner', 'users').split()

    # ------------------------------------------------------------------------------------------------------------------
    def start_job(self):
        self.__log_job_start()

        # Create pipes for stdout and stderr.
        pipe_stdout = os.pipe()
        pipe_stderr = os.pipe()

        self.__child_pid = os.fork()
        if self.__child_pid == 0:
            # Child process.
            try:
                # Close the read ends from the pipes.
                os.close(pipe_stdout[0])
                os.close(pipe_stderr[0])

                # Duplicate stdout and stderr on the pipes.
                sys.stdout.flush()
                sys.stderr.flush()
                os.dup2(pipe_stdout[1], sys.stdout.fileno())
                os.dup2(pipe_stderr[1], sys.stderr.fileno())

                # Set the effective user and group.
                if self.__user_name in self.__allowed_users:
                    _, _, uid, gid, _, _, _ = pwd.getpwnam(self.__user_name)
                    os.setuid(0)
                    os.setresgid(gid, gid, gid)
                    os.setresuid(uid, uid, uid)
                else:
                    raise RuntimeError("Spanner is not allowed to start processes under user '%s'." % self.__user_name)

                # Set variable for subprocess.
                os.putenv('ENK_RND_ID', str(self.__rnd_id))
                os.putenv('ENK_SCH_ID', str(self.__sch_id))

                # Replace this child process with the actual job.
                os.execv(self.__args[0], self.__args)

            except Exception as e:
                self.__log.error('Unable to start job')
                self.__log.error('Reason: {}'.format(str(e)))
                self.__log.exception('Error')

                # Exit immediately without running the exit handlers (e.g. from daemon) from the parent process.
                os._exit(-1)
        else:
            # Parent process.
            # Close the write ends from the pipes.
            os.close(pipe_stdout[1])
            os.close(pipe_stderr[1])

            # Remember the fds for reading the stdout and stderr from the child process.
            self.__stdout = pipe_stdout[0]
            self.__stderr = pipe_stderr[0]

            # Make reading from the pipes non-blocking.
            # fcntl.fcntl(self._stdout, 0)
            # fcntl.fcntl(self._stderr, 0)

# ----------------------------------------------------------------------------------------------------------------------
