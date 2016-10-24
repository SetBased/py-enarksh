"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import enarksh
from enarksh.DataLayer import DataLayer
from enarksh.controller.StateChange import StateChange
from enarksh.controller.resource.Resource import Resource


class ReadWriteLockResource(Resource):
    """
    Class for objects in the controller of type 'CountingResource'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, data):
        """
        Object constructor.

        :param dict data:
        """
        Resource.__init__(self, data)

        self._read_lock_count = 0
        """
        The number of consumptions that have currently a read lock on this resource.

        :type: int
        """

        self._read_write_lock_count = 0
        """
        The number of consumptions that have currently a read-write lock on this resource (0 or either 1).

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    def get_state_attributes(self):
        """
        :rtype: dict[str,int]
        """
        if self._read_write_lock_count:
            return {'rws_id': enarksh.ENK_RWS_ID_WRITE}

        if self._read_lock_count:
            return {'rws_id': enarksh.ENK_RWS_ID_READ}

        return {'rws_id': enarksh.ENK_RWS_ID_NONE}

    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def acquire(self, rws_id):
        """
        Registers that a node has currently a lock on this resource.

        :param int rws_id: The ID of the lock type.
        """
        if rws_id == enarksh.ENK_RWS_ID_READ:
            self._read_lock_count += 1

        elif rws_id == enarksh.ENK_RWS_ID_WRITE:
            self._read_write_lock_count += 1

        else:
            raise Exception("Unknown rws_id '{0!s}'.".format(rws_id))

    # ------------------------------------------------------------------------------------------------------------------
    def inquire(self, rws_id):
        """
        Returns True when it is possible the acquire a lock on this resource. Returns False otherwise.

        :param int rws_id: The ID of the lock type.

        :rtype: bool
        """
        if rws_id == enarksh.ENK_RWS_ID_READ:
            # Is is possible to acquire a read lock when no consumption has a read-write lock on this resource.
            return self._read_write_lock_count == 0

        if rws_id == enarksh.ENK_RWS_ID_WRITE:
            # Is is possible to acquire a read-write lock when no consumption has a read nor a read-write lock on this
            # resource.
            return self._read_write_lock_count == 0 and self._read_lock_count == 0

        raise Exception("Unknown rws_id '{0!s}'.".format(rws_id))

    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def release(self, rws_id):
        """
        Registers that a node has no longer a lock on this resource.

        :param int rws_id: The ID of the lock type.
        """
        if rws_id == enarksh.ENK_RWS_ID_READ:
            self._read_lock_count -= 1

        elif rws_id == enarksh.ENK_RWS_ID_WRITE:
            self._read_write_lock_count -= 1

        else:
            raise Exception("Unknown rws_id '{0!s}'.".format(rws_id))

    # ------------------------------------------------------------------------------------------------------------------
    def sync_state(self):
        if self._read_write_lock_count:
            rws_id = enarksh.ENK_RWS_ID_WRITE
        elif self._read_lock_count:
            rws_id = enarksh.ENK_RWS_ID_READ
        else:
            rws_id = enarksh.ENK_RWS_ID_NONE

        DataLayer.enk_back_read_write_lock_resource_update_consumpted(self._rsc_id, rws_id)

    # ------------------------------------------------------------------------------------------------------------------
    def get_type(self):
        """
        Return the name of the type this resource type.

        :rtype: str
        """
        return 'ReadWriteLockResource'

# ----------------------------------------------------------------------------------------------------------------------
