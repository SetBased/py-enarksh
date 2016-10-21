"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.message.Message import Message


class NodeActionWebMessage(Message):
    """
    Message type for requesting a node action made through the web application.
    """
    MESSAGE_TYPE = 'controller:NodeActionWebMessage'
    """
    The message type.

    :type: str
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, sch_id, rnd_id, act_id):
        """
        Object constructor.

        :param int sch_id: The ID of the schedule.
        :param int rnd_id: The ID of the run node.
        :param int act_id: The ID of the requested action.
        """
        Message.__init__(self, NodeActionWebMessage.MESSAGE_TYPE)

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

        self.act_id = act_id
        """
        The ID of the requested action.

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
        return NodeActionWebMessage(int(message['sch_id']),
                                    int(message['rnd_id']),
                                    int(message['act_id']))

    # ------------------------------------------------------------------------------------------------------------------
    def send_message(self, end_point):
        """
        Sends the message to an end point.

        :param str end_point: The end point.

        :rtype: None
        """
        self.message_controller.send_message(end_point, self)

# ----------------------------------------------------------------------------------------------------------------------
