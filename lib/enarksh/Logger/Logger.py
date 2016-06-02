import os
import traceback
import sys

import zmq

from lib import enarksh
from lib.enarksh.DataLayer import DataLayer


# ----------------------------------------------------------------------------------------------------------------------
class Logger:
    _instance = None

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        Logger._instance = self

        self._events = []
        """
        A list of events that needs be be processed.
        """

        self._exit_flag = False
        """
        If set the logger must terminate.
        """

        self._zmq_context = None
        """
        The ZMQ context.
        """

        self._zmq_pull_socket = None
        """
        ZMQ socket for asynchronous incoming messages.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def main(self):
        self._startup()

        while not self._exit_flag or self._events:
            try:
                self._read_messages()

                # Connect to the database and start a transaction.
                DataLayer.connect()
                DataLayer.start_transaction()

                while self._events:
                    event = self._events.pop()

                    if event['type'] == 'logfile':
                        self._event_handler_log_file(event['message'])

                    elif event['type'] == 'exit':
                        self._event_handler_exit()

                    else:
                        raise Exception("Unknown event type '%s'." % event['type'])

                # Commit the transaction and disconnect form the database.
                DataLayer.commit()
                DataLayer.disconnect()

            except Exception as exception1:
                try:
                    DataLayer.rollback()
                    DataLayer.disconnect()
                except Exception as exception2:
                    print(exception2, file=sys.stderr)
                    traceback.print_exc(file=sys.stderr)
                print(exception1, file=sys.stderr)
                traceback.print_exc(file=sys.stderr)

    # ------------------------------------------------------------------------------------------------------------------
    def _add_event(self, event: dict) -> None:
        """
        Adds an event to the event queue.
        """
        self._events.append(event)

    # ------------------------------------------------------------------------------------------------------------------
    def _event_handler_exit(self):
        """
        Handles an exit message from the controller.
        """
        self._exit_flag = True

    # ------------------------------------------------------------------------------------------------------------------
    def _event_handler_log_file(self, message):
        """
        Handles a new log file available message from the spawner.
        """
        print("%s %s %s" % (message['rnd_id'], message['name'], message['total_size']))

        if message['total_size'] > 0:
            # Read the log file or log files and concatenate if necessary.
            with open(message['filename1'], 'rb') as f:
                log = f.read()

            if message['filename2']:
                with open(message['filename2'], 'rb') as f:
                    buf2 = f.read()
            else:
                buf2 = ''

            # Compute the number of skipped bytes.
            skipped = message['total_size'] - len(log) - len(buf2)

            if skipped != 0:
                # Add a newline to the end of the buffer, if required.
                if log[-1:] != "\n":
                    log += "\n"

                    # Note: This concatenation doesn't work for multi byte character sets.
                    log += "\n"
                    log += "Enarksh: Skipped $skipped bytes.\n"
                    log += "\n"

                log += buf2

            blb_id = DataLayer.enk_blob_insert_blob(message['name'], 'text/plain', log)

        else:
            blb_id = None

        if message['name'] == 'out':
            DataLayer.enk_back_run_node_update_log(message['rnd_id'], blb_id, message['total_size'])
        elif message['name'] == 'err':
            DataLayer.enk_back_run_node_update_err(message['rnd_id'], blb_id, message['total_size'])
        else:
            raise Exception("Unknown output name '%s'." % message['name'])

        # Remove the (temporary) log files.
        if message['filename1']:
            os.unlink(message['filename1'])
        if message['filename2']:
            os.unlink(message['filename2'])

    # ------------------------------------------------------------------------------------------------------------------
    def _read_messages(self):
        """
        Reads messages from other processes (i.e. spawner and controller).
        """
        message = self._zmq_pull_socket.recv_json()

        if message['type'] == 'log_file':
            event = {'type': 'logfile',
                     'message': message}
            self._add_event(event)

        elif message['type'] == 'exit':
            event = {'type': 'exit'}
            self._add_event(event)

        else:
            raise Exception("Unknown event type '%s'." % message['type'])

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _create_pid_file():
        """
        Creates a PID file and writes the PID of the logger to this file.
        """
        filename = enarksh.ENK_LOCK_DIR + 'logger.pid'
        with open(filename, 'w') as f:
            f.write(str(os.getpid()))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _remove_pid_file():
        """
        Removes the PID file.
        """
        filename = enarksh.ENK_LOCK_DIR + 'logger.pid'
        os.unlink(filename)

    # ------------------------------------------------------------------------------------------------------------------
    def _shutdown(self) -> None:
        """
        Performs the necessary actions for stopping the logger.
        """
        # Commit the last transaction and close the connection to the database.
        DataLayer.commit()
        DataLayer.disconnect()

        # Remove the PID file.
        self._remove_pid_file()

        # Log stop of the logger.
        print('Stop logger')

    # ------------------------------------------------------------------------------------------------------------------
    def _startup(self) -> None:
        """
        Performs the necessary actions for starting up the logger.
        """
        # Log the start of the logger.
        print('Start logger')

        # Set database configuration options.
        DataLayer.config['host'] = enarksh.MYSQL_HOSTNAME
        DataLayer.config['user'] = enarksh.MYSQL_USERNAME
        DataLayer.config['password'] = enarksh.MYSQL_PASSWORD
        DataLayer.config['database'] = enarksh.MYSQL_SCHEMA
        DataLayer.config['port'] = enarksh.MYSQL_PORT

        # Setup ZMQ.
        self._zmq_init()

        # Create our PID file.
        self._create_pid_file()

    # ------------------------------------------------------------------------------------------------------------------
    def _zmq_init(self) -> None:
        """
        Initializes the ZMQ socket.
        """
        self._zmq_context = zmq.Context()

        # Create socket for asynchronous incoming messages.
        self._zmq_pull_socket = self._zmq_context.socket(zmq.PULL)
        self._zmq_pull_socket.bind(enarksh.LOGGER_PULL_END_POINT)


# ----------------------------------------------------------------------------------------------------------------------
