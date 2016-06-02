from lib import enarksh
from lib.enarksh.Controller.Resource import Resource
from lib.enarksh.Controller.Resource.CountingResource import CountingResource
from lib.enarksh.Controller.Resource.ReadWriteLockResource import ReadWriteLockResource


# ----------------------------------------------------------------------------------------------------------------------
def create_resource(data: dict) -> Resource:
    """
    A factory for creating a resource.

    :param data: The parameters required for creating the resource.
    :return:
    """
    if data['rtp_id'] == enarksh.ENK_RTP_ID_COUNTING:
        return CountingResource(data)

    if data['rtp_id'] == enarksh.ENK_RTP_ID_READ_WRITE:
        return ReadWriteLockResource(data)

    raise Exception("Unexpected resource type ID '%s'.", data['rtp_id'])


# ----------------------------------------------------------------------------------------------------------------------
