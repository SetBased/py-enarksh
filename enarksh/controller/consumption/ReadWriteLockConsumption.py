"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.controller.consumption.Consumption import Consumption


class ReadWriteLockConsumption(Consumption):
    """
    Class for objects in the controller of type 'ReadWriteLockConsumption'.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, data, host_resources, schedule_resources):
        """
        Object constructor

        :param dict data:
        :param dict host_resources:
        :param dict schedule_resources:
        """
        Consumption.__init__(self, data, host_resources, schedule_resources)

        self.rws_id = data['rws_id']
        """
        The amount consumpted by this ReadWriteLockConsumption.

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    def acquire_resource(self):
        """
        Returns None.

        :rtype: None
        """
        return self._resource.acquire(self.rws_id)

    # ------------------------------------------------------------------------------------------------------------------
    def inquire_resource(self):
        """
        Returns None.

        :rtype: bool
        """
        return self._resource.inquire(self.rws_id)

    # ------------------------------------------------------------------------------------------------------------------
    def release_resource(self):
        """
        Releases the resource.
        """
        self._resource.release(self.rws_id)

# ----------------------------------------------------------------------------------------------------------------------
