"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.message.Message import Message


class NodeActionMessage(Message):
    """
    Message type for requesting a node action made through the CLI application.
    """
    MESSAGE_TYPE = 'controller:NodeActionMessage'
    """
    The message type.

    :type: str
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, uri, act_id):
        """
        Object constructor.

        :param str uri: The URI of the node for which a action is requested.
        :param int act_id: The ID of the requested action.
        """
        Message.__init__(self, NodeActionMessage.MESSAGE_TYPE)

        self.uri = uri
        """
        The URI of the node for which a action is requested.

        :type: str
        """

        self.act_id = act_id
        """
        The ID of the requested action.

        :type: int
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
