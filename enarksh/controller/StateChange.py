"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc

from enarksh.event.Event import Event
from enarksh.event.EventActor import EventActor


class StateChange(EventActor, metaclass=abc.ABCMeta):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        EventActor.__init__(self)

        self.event_state_change = Event(self)
        """
        The event that will be fired when the state of this object has changed.

        :type: enarksh.event.Event.Event
        """

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_state_attributes(self):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def wrapper(func):
        def inner(*args, **kwargs):
            obj = args[0]

            # Save the old state of the object.
            old = obj.get_state_attributes()

            # Run the actual method.
            ret = func(*args, **kwargs)

            # Save the new state of the object.
            new = obj.get_state_attributes()

            # If state has changed inform all observers.
            if old != new:
                obj.event_state_change.fire((old, new))

            return ret

        return inner

# ----------------------------------------------------------------------------------------------------------------------
