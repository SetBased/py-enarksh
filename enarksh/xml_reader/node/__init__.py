from enarksh.xml_reader.node.CommandJobNode import CommandJobNode
from enarksh.xml_reader.node.CompoundJobNode import CompoundJobNode
from enarksh.xml_reader.node.DynamicInnerWorkerNode import DynamicInnerWorkerNode
from enarksh.xml_reader.node.DynamicJobNode import DynamicJobNode
from enarksh.xml_reader.node.DynamicOuterWorkerNode import DynamicOuterWorkerNode
from enarksh.xml_reader.node.ManualTriggerNode import ManualTriggerNode
from enarksh.xml_reader.node.Node import Node
from enarksh.xml_reader.node.ScheduleNode import ScheduleNode
from enarksh.xml_reader.node.TerminatorNode import TerminatorNode


# ----------------------------------------------------------------------------------------------------------------------
def create_node(tag, parent_node=None):
    """
    A factory for creating nodes.

    :param str tag:
    :param enarksh.xml_reader.node.Node.Node parent_node:

    :rtype: enarksh.xml_reader.node.Node.Node
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
