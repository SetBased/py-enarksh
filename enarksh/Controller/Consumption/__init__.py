import enarksh
from enarksh.Controller.Consumption.Consumption import Consumption
from enarksh.Controller.Consumption.CountingConsumption import CountingConsumption
from enarksh.Controller.Consumption.ReadWriteLockConsumption import ReadWriteLockConsumption


# ----------------------------------------------------------------------------------------------------------------------
def create_consumption(data, host_resources, schedule_resources):
    """
    A factory for creating a Consumption.

    :param dict data: The parameters required for creating the Consumption.
    :param dict host_resources:
    :param dict schedule_resources:

    :rtype: enarksh.Controller.Consumption.Consumption.Consumption
    """
    if data['ctp_id'] == enarksh.ENK_CTP_ID_COUNTING:
        return CountingConsumption(data, host_resources, schedule_resources)

    if data['ctp_id'] == enarksh.ENK_CTP_ID_READ_WRITE:
        return ReadWriteLockConsumption(data, host_resources, schedule_resources)

    raise Exception("Unexpected Consumption type ID '%s'.", data['ctp_id'])


# ----------------------------------------------------------------------------------------------------------------------
