"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc


class Message(metaclass=abc.ABCMeta):
    """
    Class for messages exchanged between the processes of Enarksh.
    """

    # ------------------------------------------------------------------------------------------------------------------
    message_controller = None
    """
    The message controller.

    :type: None|enarksh.message.MessageController.MessageController
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, message_type):
        """
        Object constructor.
        """
        self._message_type = message_type
        """
        The type of the message.

        :type: str
        """

        self.message_source = None
        """
        For incoming messages the name of the source of the message. This field will be set by the message controller.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def message_type(self):
        """
        Returns the message type of this message.

        :rtype: str
        """
        return self._message_type

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def send_message(self, end_point):
        """
        Sends the message to an end point.

        :param str end_point: The end point.

        :rtype: None|enarksh.message.Message.Message
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
