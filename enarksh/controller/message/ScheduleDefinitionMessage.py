"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.message.Message import Message


class ScheduleDefinitionMessage(Message):
    """
    Message type for loading a new schedule definition.
    """
    MESSAGE_TYPE = 'controller:ScheduleDefinitionMessage'
    """
    The message type.

    :type: str
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, xml, filename):
        """
        Object constructor.

        :param str xml: The XML with the schedule definition.
        :param str filename: The name of the file with the schedule definition.
        """
        Message.__init__(self, ScheduleDefinitionMessage.MESSAGE_TYPE)

        self.xml = xml
        """
        The XML with the schedule definition.

        :type: str
        """

        self.filename = filename
        """
        The name of the file with the schedule definition.

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
