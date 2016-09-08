"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.message.Message import Message


class DynamicWorkerDefinitionMessage(Message):
    """
    Message type for loading a dynamic worker definition.
    """
    MESSAGE_TYPE = 'controller:DynamicWorkerDefinitionMessage'
    """
    The message type.

    :type: str
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, sch_id, rnd_id, xml):
        """
        Object constructor.

        :param int sch_id: The ID of the schedule.
        :param int rnd_id: The ID of the run node.
        :param int xml: The XML with the dynamic worker definition.
        """
        Message.__init__(self, DynamicWorkerDefinitionMessage.MESSAGE_TYPE)

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

        self.xml = xml
        """
        The XML with the dynamic worker definition.

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
