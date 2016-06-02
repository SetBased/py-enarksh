from lib.enarksh.Controller.Consumption.Consumption import Consumption


# ----------------------------------------------------------------------------------------------------------------------
class CountingConsumption(Consumption):
    """
    Consumption of a node.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, data: dict, host_resources: dict, schedule_resources: dict):
        Consumption.__init__(self, data, host_resources, schedule_resources)

        self.amount_Consumption = data['cns_amount']
        """
        The amount consumpted by this Consumption.

        :type int
        """

    # ------------------------------------------------------------------------------------------------------------------
    def acquire_resource(self) -> None:
        return self._resource.acquire(self.amount_Consumption)

    # ------------------------------------------------------------------------------------------------------------------
    def inquire_resource(self) -> bool:
        return self._resource.inquire(self.amount_Consumption)

    # ------------------------------------------------------------------------------------------------------------------
    def release_resource(self) -> None:
        self._resource.release(self.amount_Consumption)

# ----------------------------------------------------------------------------------------------------------------------
