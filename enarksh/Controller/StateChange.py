"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc


class StateChange(metaclass=abc.ABCMeta):
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._observers = []
        """
        The objects that observe the state of this object.

        :type: list
        """

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_state_attributes(self):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def register_observer(self, method, **args):
        """
        Registers an object as an observer of the state of this object.

        :param method:
        :param dict args:
        """
        self._observers.append((method, args))

    # ------------------------------------------------------------------------------------------------------------------
    def unregister_all_observers(self):
        """
        Unregisters all observers.
        """
        self._observers = []

    # ------------------------------------------------------------------------------------------------------------------
    def notify_observer(self, old, new):
        """
        Notifies all observer about the state change of this object.

        :param dict old:
        :param dict new:
        """
        for (method, args) in self._observers:
            method(self, old, new, *args)

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
                obj.notify_observer(old, new)

            return ret

        return inner

# ----------------------------------------------------------------------------------------------------------------------
