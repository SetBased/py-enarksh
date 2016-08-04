"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import os

from enarksh.controller.message.JobFinishedMessage import JobFinishedMessage


class SIGCHLDEventHandler:
    """
    An event handler when SIGCHLD has been received.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, _event_data, spawner):
        """
        Handles an exit of a child and ends a job handler.

        :param * _event: Not used.
        :param * _event_data: Not used.
        :param enarksh.spawner.Spawner.Spawner spawner: The spawner.
        """
        del _event, _event_data

        try:
            pid = -1
            while pid != 0:
                pid, status = os.waitpid(-1, os.WNOHANG + os.WUNTRACED + os.WCONTINUED)
                if pid != 0:
                    job_handler = spawner.job_handlers[pid]

                    # Send message to controller that a job has finished.
                    message = JobFinishedMessage(job_handler.sch_id, job_handler.rnd_id, status)
                    message.send_message('controller')

                    # Inform the job handler the job has finished.
                    job_handler.set_job_has_finished()
        except OSError:
            # Ignore OSError. No more children to wait for.
            pass

# ----------------------------------------------------------------------------------------------------------------------
