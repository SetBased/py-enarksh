"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.message.Message import Message


class ExitMessage(Message):
    """
    Message type for instructing a process of Enarksh to exit.
    """
    MESSAGE_TYPE = 'ExitMessage'
    """
    The message type.

    :type: str
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        Message.__init__(self, ExitMessage.MESSAGE_TYPE)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_message(_):
        """
        Create a message of this class based on JSON data.

        :rtype: enarksh.message.ExitMessage.ExitMessage
        """
        return ExitMessage()

    # ------------------------------------------------------------------------------------------------------------------
    def send_message(self, end_point):
        """
        Sends the message to an end point.

        :param str end_point: The end point.

        :rtype: None
        """
        self.message_controller.send_message(end_point, self)

# ----------------------------------------------------------------------------------------------------------------------
