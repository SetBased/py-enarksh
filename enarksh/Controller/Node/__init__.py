# ----------------------------------------------------------------------------------------------------------------------
import enarksh
from enarksh.Controller.Node.CommandJobNode import CommandJobNode
from enarksh.Controller.Node.CompoundJobNode import CompoundJobNode
from enarksh.Controller.Node.DynamicJobNode import DynamicJobNode
from enarksh.Controller.Node.DynamicInnerWorkerNode import DynamicInnerWorkerNode
from enarksh.Controller.Node.DynamicOuterWorkerNode import DynamicOuterWorkerNode
from enarksh.Controller.Node.ManualTriggerNode import ManualTriggerNode
from enarksh.Controller.Node.Node import Node
from enarksh.Controller.Node.ScheduleNode import ScheduleNode
from enarksh.Controller.Node.TerminatorNode import TerminatorNode


# ----------------------------------------------------------------------------------------------------------------------
def create_node(data):
    """
    A factory for creating nodes.

    :param dict data: The parameters required for creating the node.

    :rtype: enarksh.Controller.Node.Node.Node
    """

    if data['ntp_id'] == enarksh.ENK_NTP_SCHEDULE:
        return ScheduleNode(data)

    if data['ntp_id'] == enarksh.ENK_NTP_COMMAND_JOB:
        return CommandJobNode(data)

    if data['ntp_id'] == enarksh.ENK_NTP_COMPOUND_JOB:
        return CompoundJobNode(data)

    if data['ntp_id'] == enarksh.ENK_NTP_MANUAL_TRIGGER:
        return ManualTriggerNode(data)

    if data['ntp_id'] == enarksh.ENK_NTP_TERMINATOR:
        return TerminatorNode(data)

    if data['ntp_id'] == enarksh.ENK_NTP_DYNAMIC_JOB:
        return DynamicJobNode(data)

    if data['ntp_id'] == enarksh.ENK_NTP_DYNAMIC_OUTER_WORKER:
        return DynamicOuterWorkerNode(data)

    if data['ntp_id'] == enarksh.ENK_NTP_DYNAMIC_INNER_WORKER:
        return DynamicInnerWorkerNode(data)

    raise Exception("Unexpected node type ID '%s'.", data['ntp_id'])

# ----------------------------------------------------------------------------------------------------------------------

