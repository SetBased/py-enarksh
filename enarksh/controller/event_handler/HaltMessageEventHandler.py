"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.event.Event import Event


class HaltMessageEventHandler:
    """
    An event handler for a HaltMessage received events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, _message, _listener_data):
        """
        Handles a HaltMessage received event.

        :param * _event: Not used.
        :param * _message: Not used.
        :param * _listener_data: Not used.
        """
        del _event, _message, _listener_data

        Event.event_controller.exit = True

# ----------------------------------------------------------------------------------------------------------------------
