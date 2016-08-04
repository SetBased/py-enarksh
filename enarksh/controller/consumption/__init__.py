import enarksh
from enarksh.controller.consumption.Consumption import Consumption
from enarksh.controller.consumption.CountingConsumption import CountingConsumption
from enarksh.controller.consumption.ReadWriteLockConsumption import ReadWriteLockConsumption


# ----------------------------------------------------------------------------------------------------------------------
def create_consumption(data, host_resources, schedule_resources):
    """
    A factory for creating a Сonsumption.

    :param dict data: The parameters required for creating the Сonsumption.
    :param dict host_resources:
    :param dict schedule_resources:

    :rtype: enarksh.controller.consumption.Consumption.Consumption
    """
    if data['ctp_id'] == enarksh.ENK_CTP_ID_COUNTING:
        return CountingConsumption(data, host_resources, schedule_resources)

    if data['ctp_id'] == enarksh.ENK_CTP_ID_READ_WRITE:
        return ReadWriteLockConsumption(data, host_resources, schedule_resources)

    raise Exception("Unexpected consumption type ID '%s'.", data['ctp_id'])

# ----------------------------------------------------------------------------------------------------------------------
