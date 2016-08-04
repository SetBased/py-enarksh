import enarksh
from enarksh.xml_reader.resource.CountingResource import CountingResource
from enarksh.xml_reader.resource.ReadWriteLockResource import ReadWriteLockResource
from enarksh.xml_reader.resource.Resource import Resource


# ----------------------------------------------------------------------------------------------------------------------
def create_resource(rtp_id, rsc_id, node):
    """
    A factory for creating nodes.

    :param rtp_id:
    :param rsc_id:
    :param node:

    :rtype: enarksh.xml_reader.resource.Resource.Resource
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
