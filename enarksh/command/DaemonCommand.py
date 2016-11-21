"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import logging
import logging.handlers
import os
import sys

from cleo import Command
from daemon import DaemonContext
from lockfile.pidlockfile import PIDLockFile

from enarksh.C import C
from enarksh.Config import Config
from enarksh.style.EnarkshStyle import EnarkshStyle


class DaemonCommand(Command):
    """
    Base class for commands for daemons.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def handle_daemon(self, name, daemon):
        """
        Executes the daemon command.

        :param str name: The name of the daemon.
        :param * daemon: The daemon, i.e. object with main method.
        """
        self.output = EnarkshStyle(self.input, self.output)

        log = logging.getLogger('enarksh')
        log.setLevel(logging.INFO)
        log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if self.option('daemonize'):
            config = Config.get()

            log_file_name = os.path.join(C.HOME, config.get_enarksh_log_dir(), name + '.log')
            pid_file_name = os.path.join(C.HOME, config.get_enarksh_lock_dir(), name + '.pid')

            log_handler = logging.handlers.RotatingFileHandler(log_file_name,
                                                               maxBytes=config.get_enarksh_max_log_size(),
                                                               backupCount=config.get_enarksh_log_back())
            log_handler.setLevel(logging.DEBUG)
            log_handler.setFormatter(log_formatter)
            log.addHandler(log_handler)

            output = open(log_file_name, 'ab', 0)

            context = DaemonContext()
            context.working_directory = C.HOME
            context.umask = 0o002
            context.pidfile = PIDLockFile(pid_file_name, False)
            context.stdout = output
            context.stderr = output
            context.files_preserve = [log_handler.stream]

            with context:
                daemon.main()
        else:
            log_handler = logging.StreamHandler(sys.stdout)
            log_handler.setLevel(logging.DEBUG)
            log_handler.setFormatter(log_formatter)
            log.addHandler(log_handler)

            daemon.main()

# ----------------------------------------------------------------------------------------------------------------------
