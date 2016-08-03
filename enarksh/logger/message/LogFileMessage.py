"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.message.Message import Message


class LogFileMessage(Message):
    """
    Message type for notifying the logger that a log file is available for storing into the database.
    """
    MESSAGE_TYPE = 'logger:LogFileMessage'
    """
    The message type.

    :type: str
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, rnd_id, name, total_size, filename1, filename2):
        """
        Object constructor.

        :param int rnd_id: The ID of the run node.
        :param str name: The name of he output:
                         - 'out' for stdout
                         - 'err' for stderr
        :param int total_size: The total size in bytes of the log.
        :param str|None filename1: The name of the file where the first chunk of the log is stored.
        :param str|None filename2: The name of the file where the last chunk of the log is stored.
        """
        Message.__init__(self, LogFileMessage.MESSAGE_TYPE)

        self.rnd_id = rnd_id
        """
        The ID of the run node.

        :type: int
        """

        self.name = name
        """
        The name of he output:
        - 'out' for stdout
        - 'err' for stderr

        :type: str
        """

        self.total_size = total_size
        """
        The total size in bytes of the log.

        :type: int
        """

        self.filename1 = filename1
        """
        The name of the file where the first chunk of the log is stored.

        :type: str
        """

        self.filename2 = filename2
        """
        The name of the file where the last chunk of the log is stored.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def send_message(self, end_point):
        """
        Sends the message to an end point.

        :param str end_point: The end point.

        :rtype: None
        """
        self.message_controller.send_message(end_point, self)

# ----------------------------------------------------------------------------------------------------------------------
