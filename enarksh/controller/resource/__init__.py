import enarksh
from enarksh.controller.resource import Resource
from enarksh.controller.resource.CountingResource import CountingResource
from enarksh.controller.resource.ReadWriteLockResource import ReadWriteLockResource


# ----------------------------------------------------------------------------------------------------------------------
def create_resource(data):
    """
    A factory for creating a resource.

    :param dict data: The parameters required for creating the resource.

    :rtype: enarksh.controller.resource.Resource.Resource
    """
    if data['rtp_id'] == enarksh.ENK_RTP_ID_COUNTING:
        return CountingResource(data)

    if data['rtp_id'] == enarksh.ENK_RTP_ID_READ_WRITE:
        return ReadWriteLockResource(data)

    raise Exception("Unexpected resource type ID '%s'.", data['rtp_id'])

# ----------------------------------------------------------------------------------------------------------------------
