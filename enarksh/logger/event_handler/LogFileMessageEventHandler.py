"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import logging
import os

from enarksh.DataLayer import DataLayer


class LogFileMessageEventHandler:
    """
    An event handler for a LogFileMessage received events.
    """

    @staticmethod
    # ------------------------------------------------------------------------------------------------------------------
    def handle(_event, message, _listener_data):
        """
        Handles a LogFileMessage received event.

        :param * _event: Not used.
        :param enarksh.message.logger.LogFileMessage.LogFileMessage message: The message.
        :param * _listener_data: Not used.
        """
        del _event, _listener_data

        log = logging.getLogger('enarksh')
        log.info('rnd_id: {}, name: {}, size: {}'.format(message.rnd_id, message.name, message.total_size))

        DataLayer.connect()

        if message.total_size > 0:
            # Read the log file or log files and concatenate if necessary.
            with open(message.filename1, 'rb') as file1:
                log = file1.read()

            if message.filename2:
                with open(message.filename2, 'rb') as file2:
                    buf2 = file2.read()
            else:
                buf2 = ''

            # Compute the number of skipped bytes.
            skipped = message.total_size - len(log) - len(buf2)

            if skipped != 0:
                # Add a newline to the end of the buffer, if required.
                if log[-1:] != b'\n':
                    log += b'\n'

                    # Note: This concatenation doesn't work for multi byte character sets.
                    log += b'\n'
                    log += bytes("Enarksh: Skipped {0} bytes.\n".format(skipped), 'utf8')
                    log += b'\n'

                log += buf2

            blb_id = DataLayer.enk_blob_insert_blob(message.name, 'text/plain', log)

        else:
            blb_id = None

        if message.name == 'out':
            DataLayer.enk_back_run_node_update_log(message.rnd_id, blb_id, message.total_size)
        elif message.name == 'err':
            DataLayer.enk_back_run_node_update_err(message.rnd_id, blb_id, message.total_size)
        else:
            raise ValueError("Unknown output name '%s'" % message.name)

        # Remove the (temporary) log files.
        if message.filename1:
            os.unlink(message.filename1)
        if message.filename2:
            os.unlink(message.filename2)

        DataLayer.commit()
        DataLayer.disconnect()

# ----------------------------------------------------------------------------------------------------------------------
