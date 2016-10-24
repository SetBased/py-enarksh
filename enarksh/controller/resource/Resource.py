"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc

from enarksh.controller.StateChange import StateChange


class Resource(StateChange, metaclass=abc.ABCMeta):
    """
    Class for objects in the controller of type 'Resource'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, data):
        """
        Object constructor.

        :param dict[str,*] data:
        """
        StateChange.__init__(self)

        self._name = str(data['rsc_name'], 'utf-8')  # @todo XXX pystratum
        """
        The name of this resource.

        :type: int
        """

        self._rsc_id = data['rsc_id']
        """
        The ID of this resource.

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def name(self):
        """
        Returns the name of this resource.

        :rtype: str
        """
        return self._name

    # ------------------------------------------------------------------------------------------------------------------
    def rsc_id(self):
        """
        Returns the ID of this resource.

        :rtype: str
        """
        return self._rsc_id

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def acquire(self, *args):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def inquire(self, *args):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def release(self, *args):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def sync_state(self):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_type(self):
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
