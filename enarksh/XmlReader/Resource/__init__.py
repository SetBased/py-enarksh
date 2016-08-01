import enarksh
from enarksh.XmlReader.Resource.CountingResource import CountingResource
from enarksh.XmlReader.Resource.ReadWriteLockResource import ReadWriteLockResource
from enarksh.XmlReader.Resource.Resource import Resource


# ----------------------------------------------------------------------------------------------------------------------
def create_resource(rtp_id, rsc_id, node):
    """
    A factory for creating nodes.

    :param rtp_id:
    :param rsc_id:
    :param node:

    :rtype: enarksh.XmlReader.Resource.Resource.Resource
    """
    if rtp_id == enarksh.ENK_RTP_ID_COUNTING:
        resource = CountingResource(node)

    elif rtp_id == enarksh.ENK_RTP_ID_READ_WRITE:
        resource = ReadWriteLockResource(node)

    else:
        raise Exception("Unexpected resource type ID '%s'.", rtp_id)

    resource.load_db(rsc_id)

    return resource


# ----------------------------------------------------------------------------------------------------------------------
