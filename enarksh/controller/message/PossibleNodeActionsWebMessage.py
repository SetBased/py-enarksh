"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.message.Message import Message


class PossibleNodeActionsWebMessage(Message):
    """
    Message type for requesting all possible node actions for a run node made through the web application.
    """
    MESSAGE_TYPE = 'controller:PossibleNodeActionsWebMessage'
    """
    The message type.

    :type: str
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, sch_id, rnd_id):
        """
        Object constructor.

        :param int sch_id: The ID of the schedule.
        :param int rnd_id: The ID of the run node.
        """
        Message.__init__(self, PossibleNodeActionsWebMessage.MESSAGE_TYPE)

        self.sch_id = sch_id
        """
        The ID of the schedule.

        :type: int
        """

        self.rnd_id = rnd_id
        """
        The ID of the run node.

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_from_json(message):
        """
        Object constructor using JSON encoded message.

        :param * message: The message.

        :rtype: enarksh.controller.message.PossibleNodeActionsWebMessage.PossibleNodeActionsWebMessage
        """
        return PossibleNodeActionsWebMessage(int(message['sch_id']), int(message['rnd_id']))

    # ------------------------------------------------------------------------------------------------------------------
    def send_message(self, end_point):
        """
        Sends the message to an end point.

        :param str end_point: The end point.

        :rtype: None
        """
        self.message_controller.send_message(end_point, self)

# ----------------------------------------------------------------------------------------------------------------------
