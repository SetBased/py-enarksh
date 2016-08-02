import os
import sys

# ----------------------------------------------------------------------------------------------------------------------
HOME = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

CONTROLLER_PULL_END_POINT = 'tcp://127.0.0.1:7771'
CONTROLLER_LOCKSTEP_END_POINT = 'tcp://127.0.0.1:7772'
LOGGER_PULL_END_POINT = 'tcp://127.0.0.1:7773'
SPAWNER_PULL_END_POINT = 'tcp://127.0.0.1:7774'

MYSQL_HOSTNAME = '127.0.0.1'
MYSQL_USERNAME = 'enarksh_owner'
MYSQL_PASSWORD = 'cH5thast2stebeT3'
MYSQL_SCHEMA = 'enarksh'
MYSQL_PORT = 3306

CHUNK_SIZE = 1024 * 1024

ENK_RST_ID_COMPLETED = 3
ENK_RST_ID_ERROR = 4
ENK_RST_ID_QUEUED = 5
ENK_RST_ID_RUNNING = 2
ENK_RST_ID_WAITING = 1

ENK_ACT_ID_TRIGGER = 1
ENK_ACT_ID_RESTART = 2
ENK_ACT_ID_RESTART_FAILED = 3

ENK_PTT_ID_INPUT = 1
ENK_PTT_ID_OUTPUT = 2

ENK_RWS_ID_NONE = 1
ENK_RWS_ID_READ = 2
ENK_RWS_ID_WRITE = 3

ENK_RTP_ID_COUNTING = 1
ENK_RTP_ID_READ_WRITE = 2

ENK_CTP_ID_COUNTING = 1
ENK_CTP_ID_READ_WRITE = 2

ENK_NTP_SCHEDULE = 1
ENK_NTP_COMMAND_JOB = 2
ENK_NTP_COMPOUND_JOB = 3
ENK_NTP_MANUAL_TRIGGER = 4
ENK_NTP_TERMINATOR = 5
ENK_NTP_DYNAMIC_JOB = 6
ENK_NTP_DYNAMIC_OUTER_WORKER = 7
ENK_NTP_DYNAMIC_INNER_WORKER = 8

ENK_MESSAGE_ADMIN_DIR = os.path.join(HOME, 'var/lib/message/admin')
ENK_MESSAGE_CONTROLLER_DIR = os.path.join(HOME, 'var/lib/message/controller')
ENK_MESSAGE_LOGGER_DIR = os.path.join(HOME, 'var/lib/message/logger')
ENK_MESSAGE_SPAWNER_DIR = os.path.join(HOME, 'var/lib/message/spawner')
ENK_LOCK_DIR = os.path.join(HOME, 'var/lock')


# ----------------------------------------------------------------------------------------------------------------------
def daemonize(pid_filename, stdin, stdout, stderr):
    """
    Turns the current process into a daemon process.

    Note: Call this function before opening files or create (database) connections.

    :param str pid_filename: The filename where the PID of the daemon process must be stored.
    :param str stdin:
    :param str stdout:
    :param str stderr:
    """
    if os.path.exists(pid_filename):
        file = open(pid_filename, 'r')
        pid = file.read()
        try:
            os.kill(int(pid), 0)
            # No exception. This means a process with pid is already running.
            raise RuntimeError('Already running')
        except ProcessLookupError:
            # Ignore No such process error. This means process it not running.
            pass

    # Fork the current process (detaches from parent)
    if os.fork() > 0:
        # Exit the parent process.
        raise SystemExit(0)

    # Change the working directory.
    os.chdir(HOME)

    # Reset the file mode mask.
    os.umask(0)

    # Become the session leader.
    os.setsid()

    # Flush I/O buffers
    sys.stdout.flush()
    sys.stderr.flush()

    # Replace file descriptors for stdin, stdout, and stderr
    with open(stdin, 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

    # Write the PID file
    with open(pid_filename, 'w') as f:
        print(os.getpid(), file=f)

# ----------------------------------------------------------------------------------------------------------------------
