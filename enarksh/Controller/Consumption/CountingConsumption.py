"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.Controller.Consumption.Consumption import Consumption


class CountingConsumption(Consumption):
    """
    Consumption of a node.
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

        self.amount_Consumption = data['cns_amount']
        """
        The amount consumpted by this Consumption.

        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    def acquire_resource(self):
        """
        Returns None.

        :rtype: None
        """
        return self._resource.acquire(self.amount_Consumption)

    # ------------------------------------------------------------------------------------------------------------------
    def inquire_resource(self):
        """
        Returns bool.

        :rtype: bool
        """
        return self._resource.inquire(self.amount_Consumption)

    # ------------------------------------------------------------------------------------------------------------------
    def release_resource(self):
        """
        Releases the resource.
        """
        self._resource.release(self.amount_Consumption)

# ----------------------------------------------------------------------------------------------------------------------
