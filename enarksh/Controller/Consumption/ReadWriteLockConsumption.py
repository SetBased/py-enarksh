"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.Controller.Consumption.Consumption import Consumption


class ReadWriteLockConsumption(Consumption):
    """
    Class for objects in the controller of type 'ReadWriteLockConsumption'.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, data: dict, host_resources: dict, schedule_resources: dict):
        Consumption.__init__(self, data, host_resources, schedule_resources)

        self.rws_id = data['rws_id']
        """
        The amount consumpted by this ReadWriteLockConsumption.

        :type int
        """

    # ------------------------------------------------------------------------------------------------------------------
    def acquire_resource(self) -> None:
        return self._resource.acquire(self.rws_id)

    # ------------------------------------------------------------------------------------------------------------------
    def inquire_resource(self) -> bool:
        return self._resource.inquire(self.rws_id)

    # ------------------------------------------------------------------------------------------------------------------
    def release_resource(self) -> None:
        self._resource.release(self.rws_id)

# ----------------------------------------------------------------------------------------------------------------------
