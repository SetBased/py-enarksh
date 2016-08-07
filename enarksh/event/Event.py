"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import weakref


class Event:
    """
    Class for events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    event_controller = None
    """
    The event controller.

    :type: None|enarksh.event.EventController.EventController
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, source):
        """
        Object constructor.

        :param T source: The object that generates this event.
        """
        self._source = source
        """
        The object that generates this event.

        :type: enarksh.event.EventActor.EventActor
        """

        self.ref = weakref.ref(self, Event.event_controller.internal_unregister_event_ref)
        """
        The weak reference to this event.

        :type: weakref
        """

        # Register this event as an event in the current program.
        Event.event_controller.internal_register_event(self)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def source(self):
        """
        Returns the object that fires this event.

        :rtype: enarksh.event.EventActor.EventActor
        """
        return self._source

    # ------------------------------------------------------------------------------------------------------------------
    def fire(self, event_data=None):
        """
        Fires this event. That is, the event is put on the event queue of the event controller.

        Normally this method is called by the source of this event.

        :param * event_data: Additional data supplied by the event source.
        """
        Event.event_controller.internal_queue_event(self, event_data)

    # ------------------------------------------------------------------------------------------------------------------
    def register_listener(self, listener, listener_data=None):
        """
        Registers an object as a listener for this event.

        :param callable listener: An object that listen for an event.
        :param * listener_data: Additional data supplied by the listener destination.
        """
        Event.event_controller.internal_register_listener(self, listener, listener_data)

# ----------------------------------------------------------------------------------------------------------------------
