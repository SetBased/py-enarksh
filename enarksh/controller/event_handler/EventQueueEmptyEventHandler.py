"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import functools

from enarksh.DataLayer import DataLayer


class EventQueueEmptyEventHandler:
    """
    An event handler for an empty event queue.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def queue_compare(schedule1, schedule2):
        """
        Compares two schedules for sorting queued nodes.

        :param enarksh.controller.Schedule.Schedule schedule1: Schedule 1.
        :param enarksh.controller.Schedule.Schedule schedule2: Schedule 2.

        :rtype:
        """
        return schedule1.get_schedule_load() - schedule2.get_schedule_load()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __queue_handler(controller):
        """
        Starts a node that is queued and for which there are enough resources available.

        :param enarksh.controller.Controller.Controller controller: The controller.
        """
        # Return immediately if there are no loaded schedules.
        if not controller.schedules:
            return

        start = False
        schedules = sorted(controller.schedules.values(),
                           key=functools.cmp_to_key(EventQueueEmptyEventHandler.queue_compare))
        for schedule in schedules:
            queue = schedule.get_queue()
            for node in queue:
                # Inquire if there are enough resources available for the node.
                start = node.inquire_resources()
                if start:
                    span_job = node.start()

                    # If required send a message to the spanner.
                    if span_job:
                        message = node.get_start_message(schedule.sch_id)
                        controller.message_controller.send_message('spawner', message)
                    else:
                        node.stop(0)

                    # If a node has been started leave inner loop.
                    break

            # If a node has been started leave the outer loop.
            if start:
                break

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def handle(_event, _event_data, controller):
        """
        Handles an empty event queue event.

        :param  _event: The event.
        :param * _event_data: Not used.
        :param enarksh.controller.Controller.Controller controller: The controller.
        """
        del _event, _event_data

        # Try the start nodes.
        EventQueueEmptyEventHandler.__queue_handler(controller)

        DataLayer.commit()
        DataLayer.disconnect()

        # If event queue is empty listen for new messages.
        if controller.event_controller.queue_size() == 0:
            controller.message_controller.receive_message(None, None, None)

        DataLayer.connect()
        DataLayer.start_transaction()

# ----------------------------------------------------------------------------------------------------------------------
