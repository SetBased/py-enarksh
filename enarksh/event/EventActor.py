"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import weakref

from enarksh.event.Event import Event


class EventActor:
    """
    Parent class for classes that fire events and for classes that listen for events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self.ref = weakref.ref(self, Event.event_controller.internal_unregister_listener_object_ref)
        """
        The weak reference to this event actor.

        :type: weakref
        """

# ----------------------------------------------------------------------------------------------------------------------
