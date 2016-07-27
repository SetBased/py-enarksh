"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
from enarksh.Controller.Resource.Resource import Resource


# ----------------------------------------------------------------------------------------------------------------------
from enarksh.Controller.StateChange import StateChange
from enarksh.DataLayer import DataLayer


class CountingResource(Resource):
    """
    Class for objects in the controller of type 'CountingResource'.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, data: dict):
        Resource.__init__(self, data)

        self._amount = data['rsc_amount']
        """
        The amount available for this resource.

        :type int
        """

        self._amount_consumpted = 0
        """
        The amount currently consumpted.

        :type int
        """

    # ------------------------------------------------------------------------------------------------------------------
    def get_state_attributes(self):
        return {'rsc_amount_consumpted': self._amount_consumpted}

    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def acquire(self, amount: int) -> None:
        """
        Registers that an amount of this resource is currently consumpted.
        :param amount: The amount consumpted.
        """
        self._amount_consumpted += amount

    # ------------------------------------------------------------------------------------------------------------------
    def inquire(self, amount: int) -> bool:
        """
        Returns true when there is enough resource available for consumption $theAmount of this resource. Returns false
        otherwise.
        :param amount: The amount to be consumpted.
        """
        return self._amount - self._amount_consumpted >= amount

    # ------------------------------------------------------------------------------------------------------------------
    @StateChange.wrapper
    def release(self, amount: int) -> None:
        """
        Registers that an amount of this resource is no longer consumpted.
        :param amount: The amount released from this resource.
        """
        self._amount_consumpted -= amount

    # ------------------------------------------------------------------------------------------------------------------
    def sync_state(self):
        DataLayer.enk_back_counting_resource_update_consumpted(self.rsc_id, self._amount_consumpted)

    # ------------------------------------------------------------------------------------------------------------------
    def get_type(self) -> str:
        """
        Returns the name of the type of this resource type.
        """
        return 'CountingResource'


# ----------------------------------------------------------------------------------------------------------------------
