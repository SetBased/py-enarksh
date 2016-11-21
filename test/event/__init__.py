import os
import sys

# ----------------------------------------------------------------------------------------------------------------------
HOME = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

CONTROLLER_PULL_END_POINT = 'tcp://127.0.0.1:7771'
CONTROLLER_LOCKSTEP_END_POINT = 'tcp://127.0.0.1:7772'
LOGGER_PULL_END_POINT = 'tcp://127.0.0.1:7773'
SPAWNER_PULL_END_POINT = 'tcp://127.0.0.1:7774'

MYSQL_HOSTNAME = '127.0.0.1'
MYSQL_USERNAME = 'enarksh_owner'
MYSQL_PASSWORD = 'cH5thast2stebeT3'
MYSQL_SCHEMA = 'enarksh'
MYSQL_PORT = 3306

ENK_LOCK_DIR = os.path.join(HOME, 'var/lock')


# ----------------------------------------------------------------------------------------------------------------------
def daemonize(pid_filename: str, stdin: str, stdout: str, stderr: str):
    """
    Turns the current process into a daemon process.
    Note: Call this function before opening files or create (database) connections.
    :param pid_filename: The filename where the PID of the daemon process must be stored.
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
