"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.spawner.JobHandler import JobHandler
from enarksh.spawner.event_handler.JobFinallyDoneEventHandler import JobFinallyDoneEventHandler


class SpawnJobMessageEventHandler:
    """
    An event handler for a SpawnJobMessage received events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, message, spawner):
        """
        Handles a SpawnJobMessage received event.

        :param * _event: Not used.
        :param enarksh.spawner.message.SpawnJobMessage.SpawnJobMessage message: The message.
        :param enarksh.spawner.Spawner.Spawner spawner: The spawner.
        """
        del _event

        job_handler = JobHandler(message.sch_id, message.rnd_id, message.user_name, message.args)
        job_handler.start_job()
        job_handler.final_event.register_listener(JobFinallyDoneEventHandler.handle, (spawner, job_handler.pid))

        spawner.add_job_handler(job_handler)

# ----------------------------------------------------------------------------------------------------------------------
