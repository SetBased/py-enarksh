"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""


class ExitMessageEventHandler:
    """
    An event handler for a ExitMessage received events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(event, _event_data, _listener_data):
        """
        Handles a LogFileMessage received event.

        :param enarksh.event.Event.Event event: The event.
        :param * _event_data: Not used.
        :param * _listener_data: Not used.
        """
        del _event_data, _listener_data

        event.event_controller.exit = True

# ----------------------------------------------------------------------------------------------------------------------
