"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.message.Message import Message


class HaltMessage(Message):
    """
    Message type for instructing a daemon of Enarksh to halt.
    """
    MESSAGE_TYPE = 'HaltMessage'
    """
    The message type.

    :type: str
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        Message.__init__(self, HaltMessage.MESSAGE_TYPE)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_message(_):
        """
        Create a message of this class based on JSON data.

        :rtype: enarksh.message.HaltMessage.HaltMessage
        """
        return HaltMessage()

    # ------------------------------------------------------------------------------------------------------------------
    def send_message(self, end_point):
        """
        Sends the message to an end point.

        :param str end_point: The end point.

        :rtype: None
        """
        self.message_controller.send_message(end_point, self)

# ----------------------------------------------------------------------------------------------------------------------
