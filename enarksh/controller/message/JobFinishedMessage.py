"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.message.Message import Message


class JobFinishedMessage(Message):
    """
    Message type for informing the controller that a job has finished.
    """
    MESSAGE_TYPE = 'controller:JobFinishedMessage'
    """
    The message type.

    :type: str
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, sch_id, rnd_id, exit_status):
        """
        Object constructor.

        :param int sch_id: The ID of the schedule of the job.
        :param int rnd_id: The ID of the job.
        :param int exit_status: The exit status of the job.
        """
        Message.__init__(self, JobFinishedMessage.MESSAGE_TYPE)

        self.sch_id = sch_id
        """
        The ID of the schedule of the job.

        :type: int
        """

        self.rnd_id = rnd_id
        """
        The ID of the job.

        :type: int
        """

        self.exit_status = exit_status
        """
        The exit status of the job.

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
