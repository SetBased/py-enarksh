"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import logging

from enarksh.event.Event import Event
from enarksh.event.EventActor import EventActor


class EventController(EventActor):
    """
    A single threaded and a run-to-completion event controller. That is, each event is processed completely before any
    other event is processed. Hence, an event listener will run entirely before any other code runs (which can
    potentially modify the data the event listener invokes).

    Methods with name starting with 'internal_' MUST not be called from your application (only friend classes are
    allowed to call these methods).
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        Event.event_controller = self

        EventActor.__init__(self)

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

        self.exit = False
        """
        If True the event loop terminates as soon as the event queue is emtpy. No event_queue_empty event will be fired.

        :type: bool
        """

        self._queue = []
        """
        The queue with events that have fired but have not been processed yet.

        :type: list[(enarksh.event.Event.Event,*)]
        """

        self.__log = logging.getLogger('enarksh')
        """
        The logger.

        :type: logging.Logger
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
    def queue_size(self):
        """
        Returns the number of event on the event queue.

        :rtype: int
        """
        return len(self._queue)

    # ------------------------------------------------------------------------------------------------------------------
    def loop(self):
        """
        Start the event handler loop.

        The event handler loop terminates under each of the conditions below:
        * The event handler for 'event_queue_empty' completes without adding new events on the event queue.
        * Property exit has been set to True and the event queue is empty. Note: after property exit has been set to
          True event 'event_queue_empty' will not be fired any more.
        """
        self._dispatch_event(self._event_loop_start, None)

        if not self.exit and not self._queue:
            self._dispatch_event(self._event_queue_empty, None)

        while self._queue:
            event, event_data = self._queue.pop(0)

            self._dispatch_event(event, event_data)

            if not self._queue and not self.exit:
                self._dispatch_event(self._event_queue_empty, None)
                if not self._queue:
                    self.exit = True

        self._dispatch_event(self._event_loop_end, None)

    # ------------------------------------------------------------------------------------------------------------------
    def _dispatch_event(self, event, event_data):
        """
        Dispatches an event.

        :param enarksh.event.Event.Event event: The event to be dispatch.
        :param * event_data: Additional data supplied by the event source.
        """
        for listener_object, listeners in self._events[event.ref].items():
            for listener, listener_data in listeners:
                try:
                    if listener_object:
                        listener(listener_object(), event, event_data, listener_data)
                    else:
                        listener(event, event_data, listener_data)
                except Exception:
                    self.__log.exception('Error')

    # ------------------------------------------------------------------------------------------------------------------
    def internal_queue_event(self, event, event_data):
        """
        Puts an event that has fired on the event queue.

        Note: Do not use this method directly. Use enarksh.event.Event.Event.fire() instead.

        :param enarksh.event.Event.Event event: The event that has fired.
        :param * event_data: Additional data supplied by the event source.
        """
        self._queue.append((event, event_data))

    # ------------------------------------------------------------------------------------------------------------------
    def internal_unregister_event_ref(self, event_ref):
        """
        Removes an event as an event in the current program.

        Note: Do not use this method directly. Use enarksh.event.EventActor.EventActor.destroy() instead.

        :param enarksh.event.Event.Event event_ref: The event that must be removed.
        """
        if event_ref in self._events:
            for listener_object in self._events[event_ref].keys():
                events = self._listener_objects[listener_object]
                events.remove(event_ref)

                if not events:
                    del self._listener_objects[listener_object]

            del self._events[event_ref]

    # ------------------------------------------------------------------------------------------------------------------
    def internal_unregister_listener_object_ref(self, listener_object_ref):
        """
        Removes an object as a listener object (i.e. an object with one or more methods registered as event listeners).

        Note: Do not use this method directly.

        :param enarksh.event.Listener.Listener listener_object_ref: The listener object.
        """
        if listener_object_ref in self._listener_objects:
            # Remove the object from all events.
            for event in self._listener_objects[listener_object_ref]:
                del self._events[event][listener_object_ref]

            # Remove the object as listener object.
            del self._listener_objects[listener_object_ref]

    # ------------------------------------------------------------------------------------------------------------------
    def internal_register_event(self, event):
        """
        Registers an event as an event in the current program.

        Note: Do not use this method directly. This method is automatically called by
        enarksh.event.Event.Event#__init__()

        :param enarksh.event.Event.Event event: The event that must be registered.
        """
        self._events[event.ref] = dict()

    # ------------------------------------------------------------------------------------------------------------------
    def internal_register_listener(self, event, listener, listener_data=None):
        """
        Registers a callable as a listener for an event.

        Note: Do not use this method directly. Use enarksh.event.Event.Event.register_listener() instead.

        :param enarksh.event.Event.Event event: The event for which the listener needs to notified.
        :param callable listener: The callable that must be called when the event fires. If the callable is a class
                                  method it object must be an instance of enarksh.event.EventActor.EventActor.
        :param listener_data: Additional data supplied by the listener. This data will be passed to the listener when
                              the event fires.
        """
        if hasattr(listener, '__self__'):
            if not isinstance(listener.__self__, EventActor):
                raise ValueError('Only an event actor can be a listener, got {0}'.format(listener.__self__))
            listener_object = listener.__self__.ref
            listener = listener.__func__
        else:
            listener_object = None

        # Register the event and the listener.
        if listener_object not in self._events[event.ref]:
            self._events[event.ref][listener_object] = list()
        self._events[event.ref][listener_object].append((listener, listener_data))

        # Register the listener's object as a listener object.
        if listener_object not in self._listener_objects:
            self._listener_objects[listener_object] = set()
        self._listener_objects[listener_object].add(event.ref)

# ----------------------------------------------------------------------------------------------------------------------
