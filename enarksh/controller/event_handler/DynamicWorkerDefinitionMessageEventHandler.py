"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import logging

from enarksh.DataLayer import DataLayer
from enarksh.xml_reader.XmlReader import XmlReader
from enarksh.xml_reader.node.FakeParent import FakeParent


class DynamicWorkerDefinitionMessageEventHandler:
    """
    An event handler for a DynamicWorkerDefinitionMessage received events.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, message, controller):
        """
        Handles a DynamicWorkerDefinitionMessage received event.

        :param * _event: Not used.
        :param enarksh.controller.message.DynamicWorkerDefinitionMessage.DynamicWorkerDefinitionMessage message: 
               The message.
        :param enarksh.controller.Controller.Controller controller: The controller.
        """
        del _event

        log = logging.getLogger('enarksh')

        try:
            log.debug('DynamicWorkerDefinitionMessageEventHandler: rnd_id: {}'.format(message.rnd_id))

            # Get info of the dynamic node.
            info = DataLayer.enk_back_run_node_get_dynamic_info_by_generator(message.rnd_id)

            schedule = controller.get_schedule_by_sch_id(message.sch_id)
            parent = FakeParent(schedule,
                                controller.host_resources,
                                info['nod_id_outer_worker'],
                                info['rnd_id_outer_worker'])

            # Validate XML against XSD.
            reader = XmlReader()
            inner_worker = reader.parse_dynamic_worker(message.xml, parent)
            name = inner_worker.name

            # Note: Dynamic node is the parent of the worker node which is the parent of the inner worker node.
            inner_worker.set_levels(info['nod_recursion_level'] + 2)

            # Store the dynamically defined inner worker node.
            inner_worker.store(info['srv_id'], 0)

            # Create dependencies between the input and output port of the worker node and its child node(s).
            DataLayer.enk_back_node_dynamic_add_dependencies(info['nod_id_outer_worker'], inner_worker.nod_id)

            # XXX trigger reload of front end

            # Unload the schedule to force a reload of the schedule with new nodes added.
            # XXX This step must be replaced with adding dependencies between the new simple nodes and existing simple
            # nodes (successors and predecessors) and register listeners for the inner node and its new child nodes.
            controller.unload_schedule(message.sch_id)

            response = {'ret':     0,
                        'message': 'Worker {} successfully loaded'.format(name)}

            DataLayer.commit()
        except Exception as exception:
            log.exception('Error')

            response = {'ret':     -1,
                        'message': str(exception)}

            DataLayer.rollback()

        # Send the message to the job.
        controller.message_controller.send_message('lockstep', response, True)

# ----------------------------------------------------------------------------------------------------------------------
