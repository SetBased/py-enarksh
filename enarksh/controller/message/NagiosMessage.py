"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.message.Message import Message


class NagiosMessage(Message):
    """
    Message type for requesting performance data for Nagios.
    """
    MESSAGE_TYPE = 'controller:NagiosMessage'
    """
    The message type.

    :type: str
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        Message.__init__(self, NagiosMessage.MESSAGE_TYPE)

    # ------------------------------------------------------------------------------------------------------------------
    def send_message(self, end_point):
        """
        Sends the message to an end point.

        :param str end_point: The end point.

        :rtype: None
        """
        self.message_controller.send_message(end_point, self)


# ----------------------------------------------------------------------------------------------------------------------
