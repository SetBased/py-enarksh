# ----------------------------------------------------------------------------------------------------------------------
import enarksh
from enarksh.controller.node.CommandJobNode import CommandJobNode
from enarksh.controller.node.CompoundJobNode import CompoundJobNode
from enarksh.controller.node.DynamicInnerWorkerNode import DynamicInnerWorkerNode
from enarksh.controller.node.DynamicJobNode import DynamicJobNode
from enarksh.controller.node.DynamicOuterWorkerNode import DynamicOuterWorkerNode
from enarksh.controller.node.ManualTriggerNode import ManualTriggerNode
from enarksh.controller.node.Node import Node
from enarksh.controller.node.ScheduleNode import ScheduleNode
from enarksh.controller.node.TerminatorNode import TerminatorNode


# ----------------------------------------------------------------------------------------------------------------------
def create_node(data):
    """
    A factory for creating nodes.

    :param dict data: The parameters required for creating the node.

    :rtype: enarksh.controller.node.Node.Node
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
