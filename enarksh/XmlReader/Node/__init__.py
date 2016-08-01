from enarksh.XmlReader.Node.DynamicInnerWorkerNode import DynamicInnerWorkerNode
from enarksh.XmlReader.Node.DynamicJobNode import DynamicJobNode
from enarksh.XmlReader.Node.DynamicOuterWorkerNode import DynamicOuterWorkerNode
from enarksh.XmlReader.Node.Node import Node
from enarksh.XmlReader.Node.CommandJobNode import CommandJobNode
from enarksh.XmlReader.Node.CompoundJobNode import CompoundJobNode
from enarksh.XmlReader.Node.ManualTriggerNode import ManualTriggerNode
from enarksh.XmlReader.Node.ScheduleNode import ScheduleNode
from enarksh.XmlReader.Node.TerminatorNode import TerminatorNode


# ----------------------------------------------------------------------------------------------------------------------
def create_node(tag, parent_node=None):
    """
    A factory for creating nodes.

    :param str tag:
    :param enarksh.XmlReader.Node.Node.Node parent_node:

    :rtype: enarksh.XmlReader.Node.Node import Node
    """
    if tag == 'Schedule':
        return ScheduleNode(parent_node)

    if tag == 'CommandJob':
        return CommandJobNode(parent_node)

    if tag == 'CompoundJob':
        return CompoundJobNode(parent_node)

    if tag == 'DynamicJob':
        return DynamicJobNode(parent_node)

    if tag == 'DynamicInnerWorker':
        return DynamicInnerWorkerNode(parent_node)

    if tag == 'DynamicOuterWorker':
        return DynamicOuterWorkerNode(parent_node)

    if tag == 'ManualTrigger':
        return ManualTriggerNode(parent_node)

    if tag == 'Terminator':
        return TerminatorNode(parent_node)

    raise Exception("Unexpected node type '%s'.", tag)

# ----------------------------------------------------------------------------------------------------------------------
