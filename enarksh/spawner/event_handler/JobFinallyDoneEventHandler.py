"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""


class JobFinallyDoneEventHandler:
    """
    The event handler for a job finally done event.
    """

    @staticmethod
    # ------------------------------------------------------------------------------------------------------------------
    def handle(_event, _event_data, listener_data):
        """
        Handles a SpawnJobMessage received event.

        :param * _event: Not used.
        :param * _event_data: Not used.
        :param (enarksh.spawner.Spawner.Spawner,int) listener_data: The spawner and the PID of the processes of the job.
        """
        del _event, _event_data

        spawner, pid = listener_data
        spawner.remove_job_handler(pid)

# ----------------------------------------------------------------------------------------------------------------------
