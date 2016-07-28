from enarksh.event.Event import Event


class Actor:
    """
    Parent class for classes that fire events and for classes that listen for events.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self.registered_events = set()
        """
        All the (active) event this object can fire.

        Note: this field MUST only be touched by the event controller.

        :type: set[enarksh.event.Event.Event]
        """

    # ------------------------------------------------------------------------------------------------------------------
    def destroy(self):
        """
        Removes this object from the event system. This as preparation for removing this object.
        """
        for event in self.registered_events:
            event.destroy()

        Event.event_controller.unregister_listener_object(self)

# ----------------------------------------------------------------------------------------------------------------------
