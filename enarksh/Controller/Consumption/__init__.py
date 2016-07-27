import enarksh
from enarksh.Controller.Consumption.Consumption import Consumption
from enarksh.Controller.Consumption.CountingConsumption import CountingConsumption
from enarksh.Controller.Consumption.ReadWriteLockConsumption import ReadWriteLockConsumption


# ----------------------------------------------------------------------------------------------------------------------
def create_consumption(data: dict, host_resources: dict, schedule_resources: dict) -> Consumption:
    """
    A factory for creating a Consumption.

    :param data: The parameters required for creating the Consumption.
    :return:
    """
    if data['ctp_id'] == enarksh.ENK_CTP_ID_COUNTING:
        return CountingConsumption(data, host_resources, schedule_resources)

    if data['ctp_id'] == enarksh.ENK_CTP_ID_READ_WRITE:
        return ReadWriteLockConsumption(data, host_resources, schedule_resources)

    raise Exception("Unexpected Consumption type ID '%s'.", data['ctp_id'])


# ----------------------------------------------------------------------------------------------------------------------
