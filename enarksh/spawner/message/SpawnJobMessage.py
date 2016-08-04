"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.message.Message import Message


class SpawnJobMessage(Message):
    """
    Message type for instructing the spanner ot spawn a new job.
    """
    MESSAGE_TYPE = 'spawner:SpawnJobMessage'
    """
    The message type.

    :type: str
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, sch_id, rnd_id, user_name, args):
        """
        Object constructor.

        :param int sch_id: The ID of the schedule of the job.
        :param int rnd_id: The ID of the job.
        :param str user_name: The user under which the job must run.
        :param list[str] args: The arguments for the job. (args[0] is the path to the executable.)
        """
        Message.__init__(self, SpawnJobMessage.MESSAGE_TYPE)

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

        self.user_name = user_name
        """
        The user under which the job must run.

        :type: str
        """

        self.args = args
        """
        The arguments for the job. (args[0] is the path to the executable.)

        :type: list[str]
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
