from enarksh.event.Event import Event


class EventActor:
    """
    Parent class for classes that fire events and for classes that listen for events.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self.friend_registered_events = set()
        """
        All the (active) events this object can fire.

        Note: This field MUST be touched by the event controller only.

        :type: set[enarksh.event.Event.Event]
        """

    # ------------------------------------------------------------------------------------------------------------------
    def destroy(self):
        """
        Removes this object from the event system. This as preparation for removing this object such that there aren't
        references (from the event system) to this object and the garbage collector can remove this object.
        """
        for event in self.friend_registered_events:
            event.destroy()

        Event.event_controller.friend_unregister_listener_object(self)

# ----------------------------------------------------------------------------------------------------------------------
