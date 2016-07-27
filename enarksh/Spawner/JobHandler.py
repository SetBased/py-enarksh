"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from configparser import ConfigParser, Error
import os
import sys
import pwd
import traceback
import enarksh
from enarksh.Spawner.ChunkLogger import ChunkLogger


class JobHandler:
    _allowed_users = []

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, sch_id: int, rnd_id: int, user_name: str, args):
        """
        Creates a job handler for starting a job.

        :param sch_id: The ID of the schedule of the job.
        :param rnd_id: The ID of the job.
        :param user_name: The user under which the job must run.
        :param args: The arguments for the job.
        """
        self._sch_id = sch_id
        self._rnd_id = rnd_id
        self._user_name = user_name
        self._args = args

        self.stdout_logger = ChunkLogger()
        self.stderr_logger = ChunkLogger()

        self._child_pid = -1
        self._stdout = -1
        self._stderr = -1

    # ------------------------------------------------------------------------------------------------------------------
    def _log_job_start(self):
        """
        Logs the starting of a job.
        """
        print("Start rnd_id: %10d, %8s, %s" % (self._rnd_id, self._user_name, str(self._args)))

    # ------------------------------------------------------------------------------------------------------------------
    def _log_job_stop(self):
        """
        Logs the end of job.
        """
        print("End   rnd_id: %10d, %8s, %s" % (self._rnd_id, self._user_name, str(self._args)))

    # ------------------------------------------------------------------------------------------------------------------
    def get_pid(self) -> int:
        """
        Returns the PID of the job. If the job is finished the pid is -1.

        :return: The PID of the job.
        """
        return self._child_pid

    # ------------------------------------------------------------------------------------------------------------------
    def get_stdout(self) -> int:
        """
        Returns the file descriptor for reading the stdout of the child process.

        :return: file descriptor
        """
        return self._stdout

    # ------------------------------------------------------------------------------------------------------------------
    def get_stderr(self) -> int:
        """
        Returns the file descriptor for reading the stderr of the child process.

        :return: file descriptor
        """
        return self._stderr

    # ------------------------------------------------------------------------------------------------------------------
    def get_sch_id(self) -> int:
        """
        Returns the ID of the schedule of the job.

        :return: sch_id
        """
        return self._sch_id

    # ------------------------------------------------------------------------------------------------------------------
    def get_rnd_id(self) -> int:
        """
        Returns the ID of the job.

        :return: rnd_id
        """
        return self._rnd_id

    # ------------------------------------------------------------------------------------------------------------------
    def set_job_has_finished(self) -> None:
        """
        Marks that the job has finished.
        """
        self._child_pid = -1

    # ------------------------------------------------------------------------------------------------------------------
    def get_logger_message(self, std: str):
        """
        Returns a message for the logger.

        :param std: log for stdout, err for stderr
        :return: The log message.
        """
        if std == 'out':
            chunk_logger = self.stdout_logger
        elif std == 'err':
            chunk_logger = self.stderr_logger
        else:
            raise Exception("Unknown output '%s'." % std)

        return {'type': 'log_file',
                'rnd_id': self._rnd_id,
                'name': std,
                'total_size': chunk_logger.get_total_log_size(),
                'filename1': chunk_logger.get_filename1(),
                'filename2': chunk_logger.get_filename2()}

    # ------------------------------------------------------------------------------------------------------------------
    def read(self, fd: int):
        """
        Reads data from the file descriptor and stores the data in a chunk logger.
        :param fd: The file descriptor.
        """
        if fd == self._stdout:
            data = os.read(fd, 1000)
            if data == b'':
                # The pipe has been closed by the child process.
                os.close(self._stdout)
                self._stdout = -1
            else:
                self.stdout_logger.write(data)

        elif fd == self._stderr:
            data = os.read(fd, 1000)
            if data == b'':
                # The pipe has been closed by the child process.
                os.close(self._stderr)
                self._stderr = -1
            else:
                self.stdout_logger.write(data)
                self.stderr_logger.write(data)

        else:
            raise Error('Unknown file descriptor %d.' % fd)

    # ------------------------------------------------------------------------------------------------------------------
    def end_job(self):
        """

        """
        self._log_job_stop()

        self.stdout_logger.close()
        self.stderr_logger.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def read_allowed_users():
        """
        Reads the user names under which enarksh is allowed to start processes.
        """
        config = ConfigParser()
        config.read(enarksh.HOME + '/etc/enarksh.cfg')

        JobHandler._allowed_users = config.get('spawner', 'users').split()

    # ------------------------------------------------------------------------------------------------------------------
    def start_job(self):
        self._log_job_start()

        # Create pipes for stdout and stderr.
        pipe_stdout = os.pipe()
        pipe_stderr = os.pipe()

        self._child_pid = os.fork()
        if self._child_pid == 0:
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
                if self._user_name in self._allowed_users:
                    _, _, uid, gid, _, _, _ = pwd.getpwnam(self._user_name)
                    os.setuid(0)

                    os.initgroups(self._user_name, gid)
                    os.setuid(uid)
                else:
                    raise SystemExit("Spanner is not allowed to start processes under user '%s'." % self._user_name)

                # Set variable for subprocess.
                os.putenv('ENK_RND_ID', str(self._rnd_id))
                os.putenv('ENK_SCH_ID', str(self._sch_id))

                # Replace this child process with the actual job.
                os.execv(self._args[0], self._args)

            except Exception as e:
                print('Unable to start job.', file=sys.stderr)
                print('Reason: %s' % e, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                exit(-1)
        else:
            # Parent process.
            # Close the write ends from the pipes.
            os.close(pipe_stdout[1])
            os.close(pipe_stderr[1])

            # Remember the fds for reading the stdout and stderr from the child process.
            self._stdout = pipe_stdout[0]
            self._stderr = pipe_stderr[0]

            # Make reading from the pipes non-blocking.
            # fcntl.fcntl(self._stdout, 0)
            # fcntl.fcntl(self._stderr, 0)


# ----------------------------------------------------------------------------------------------------------------------
