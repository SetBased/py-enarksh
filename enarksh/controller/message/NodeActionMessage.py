"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.message.Message import Message
from enarksh.message.MessageController import MessageController


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
    def __init__(self, uri, act_id, mail_on_completion, mail_on_error):
        """
        Object constructor.

        :param str uri: The URI of the (trigger) node that must be triggered.
        :param int act_id: The ID of the requested action.
        :param bool mail_on_completion: If True the user wants to receive a mail when the schedule has completed.
        :param bool mail_on_error: If True the user wants to receive a mail when an error occurs.
        """
        Message.__init__(self, NodeActionMessage.MESSAGE_TYPE)

        self.uri = uri
        """
        The URI of the (trigger) node that must be triggered.

        :type: str
        """

        self.act_id = act_id
        """
        The ID of the requested action.

        :type: int
        """

        self.mail_on_completion = mail_on_completion
        """
        If True the user wants to receive a mail when the schedule has completed.

        :type: bool
        """

        self.mail_on_error = mail_on_error
        """
        If True the user wants to receive a mail when an error occurs.

        :type: bool
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
