"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import logging
import os

from enarksh.DataLayer import DataLayer
from enarksh.xml_reader.XmlReader import XmlReader


class ScheduleDefinitionMessageEventHandler:
    """
    An event handler for a ScheduleDefinitionMessage received events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, message, controller):
        """
        Handles a JobFinishedMessage received event.

        :param * _event: Not used.
        :param enarksh.controller.message.ScheduleDefinitionMessage.ScheduleDefinitionMessage message: The message.
        :param enarksh.controller.Controller.Controller controller: The controller.
        """
        del _event

        log = logging.getLogger('enarksh')

        try:
            # Validate XML against XSD.
            reader = XmlReader()
            schedule = reader.parse_schedule(message.xml, message.filename)

            # Test schedule is currently running.
            name = schedule.name
            if name in controller.schedules:
                raise Exception("Schedule '%s' is currently running." % name)

            # Insert the XML definition as BLOB in tot the database.
            blb_id = DataLayer.enk_blob_insert_blob(os.path.basename(message.filename), 'text/xml', message.xml)
            srv_id = DataLayer.enk_reader_schedule_create_revision(blb_id, name)
            if not srv_id:
                raise Exception("Schedule '%s' is already loaded." % name)

            # Store the new schedule definition into the database.
            schedule.store(srv_id, 1)
            DataLayer.enk_back_schedule_revision_create_run(srv_id)

            response = {'ret':     0,
                        'message': "Schedule '%s' successfully loaded." % name}

            DataLayer.commit()
        except Exception:
            log.exception('Error')

            response = {'ret':     -1,
                        'message': 'Internal error'}

            DataLayer.rollback()

        # Send the message to the web interface.
        controller.message_controller.send_message('lockstep', response, True)

# ----------------------------------------------------------------------------------------------------------------------
