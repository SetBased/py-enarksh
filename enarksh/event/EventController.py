"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import sys
import traceback

from enarksh.event.Actor import Actor
from enarksh.event.Event import Event


class EventController(Actor):
    """
    A single threaded and a run-to-completion event controller. That is, each event is processed completely before any
    other event is processed. Hence, an event listener will run entirely before any other code runs (which can
    potentially modify the data the event listener invokes).
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        Actor.__init__(self)

        Event.event_controller = self

        self._events = dict()
        """
        All events in the current program.

        :type: dict[enarksh.event.Event.Event,dict[*,list[*]]]
        """

        self._listener_objects = dict()
        """

        :type: dict[*, set[enarksh.event.Event.Event]]
        """

        self._event_loop_start = Event(self)
        """
        Event that will be fired at the start of the event loop.

        :type: enarksh.event.Event.Event
        """

        self._event_loop_end = Event(self)
        """
        Event that will be fired at the end of the event loop.

        :type: enarksh.event.Event.Event
        """

        self._event_queue_empty = Event(self)
        """
        Event that will be fired when the event queue is empty.

        :type: enarksh.event.Event.Event
        """

        self._exit = False
        """
        If True the event loop terminates as soon as the event queue is emtpy. No event_queue_empty event will be fired.

        :type: bool
        """

        self._queue = []
        """
        The queue with events that have fired but have not been processed yet.

        :type: list[(enarksh.event.Event.Event,*)]
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def event_loop_end(self):
        """
        Returns the event that will be fired at the end of the event loop.

        :rtype: enarksh.event.Event.Event
        """
        return self._event_loop_end

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def event_loop_start(self):
        """
        Returns the event that will be fired at the start of the event loop.

        :rtype: enarksh.event.Event.Event
        """
        return self._event_loop_start

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def event_queue_empty(self):
        """
        Returns the event that will be fired when the event queue is empty.

        :rtype: enarksh.event.Event.Event
        """
        return self._event_queue_empty

    # ------------------------------------------------------------------------------------------------------------------
    def loop(self):
        """
        Start the event handler loop.
        """
        self._dispatch_event(self._event_loop_start, None)

        while not self._exit:
            event, event_data = self._queue.pop(0)

            self._dispatch_event(event, event_data)

            if not self._queue and not self._exit:
                self._dispatch_event(self._event_queue_empty, None)
                if not self._queue:
                    self._exit = True

        self._dispatch_event(self._event_loop_end, None)

    # ------------------------------------------------------------------------------------------------------------------
    def _dispatch_event(self, event, event_data):
        """
        Dispatches an event.

        :param enarksh.event.Event.Event event: The event to be dispatch.
        :param * event_data: Additional data supplied by the event source.
        """
        try:
            for listeners in self._events[event].values():
                for listener, listener_data in listeners:
                    listener(event, event_data, listener_data)
        except Exception as exception:
            print(exception, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    # ------------------------------------------------------------------------------------------------------------------
    def queue_event(self, event, event_data):
        """
        Puts a event that has fired on the event queue.

        Note: Do not use this method directly. Use enarksh.event.Event.Event.fire() instead.

        :param enarksh.event.Event.Event event: The event that has fired.
        :param * event_data: Additional data supplied by the event source.
        """
        self._queue.append((event, event_data))

    # ------------------------------------------------------------------------------------------------------------------
    def unregister_event(self, event):
        """
        Removes an event as an event in the current program.

        Note: Do not use this method directly. Use enarksh.event.Actor.Actor.destroy() instead.

        :param enarksh.event.Event.Event event: The event that must be removed.
        """
        if event in self._events:
            for listener_object in self._events[event].keys():
                events = self._listener_objects[listener_object]
                events.remove(event)

                if not events:
                    del self._listener_objects[listener_object]

        del self._events[event]

    # ------------------------------------------------------------------------------------------------------------------
    def unregister_listener_object(self, listener_object):
        """
        Removes an object as a listener object (i.e. an object with one or more methods registered as event listeners).

        Note: Do not use this method directly. Use enarksh.event.Actor.Actor.destroy() instead.

        :param enarksh.event.Listener.Listener listener_object: The listener object.
        """
        if listener_object in self._listener_objects:
            # Remove the object from all events.
            for event in self._listener_objects[listener_object]:
                del self._events[event][listener_object]

            # Remove the object as listener object.
            del self._listener_objects[listener_object]

    # ------------------------------------------------------------------------------------------------------------------
    def register_event(self, event):
        """
        Registers an event as, well, an event in the current program.

        Note: Do not use this method directly. This method is automatically called by
        enarksh.event.Event.Event#__init__()

        :param enarksh.event.Event.Event event: The event that must be registered.
        """
        self._events[event] = dict()

        event.source.registered_events.add(event)

    # ------------------------------------------------------------------------------------------------------------------
    def register_listener(self, event, listener, listener_data=None):
        """
        Registers an object as a listener for this event.

        Note: Do not use this method directly. Use enarksh.event.Event.Event.register_listener() instead.

        :param enarksh.event.Event.Event event: The event for which the listener needs to notified.
        :param callable listener: The method that must be called when the event has fired.
        :param listener_data: Additional data supplied by the listener.
        """
        if hasattr(listener, '__self__'):
            if not isinstance(listener.__self__, Actor):
                raise ValueError('Only an actor can be a listener, got {0}'.format(listener.__class__))
            listener_object = listener.__self__
        else:
            listener_object = None

        if listener_object not in self._events[event]:
            self._events[event][listener_object] = list()
        self._events[event][listener_object].append((listener, listener_data))

        if listener_object not in self._listener_objects:
            self._listener_objects[listener_object] = set()
        self._listener_objects[listener_object].add(event)

# ----------------------------------------------------------------------------------------------------------------------
