import abc

from lib.enarksh.Controller.StateChange import StateChange



# ----------------------------------------------------------------------------------------------------------------------
class Resource(StateChange):
    """
    Class for objects in the controller of type 'Resource'.
    """
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, data: dict):
        StateChange.__init__(self)

        self.name = str(data['rsc_name'], 'utf-8')  # XXX pystratum
        """
        The name of this resource.
        :type: int
        """

        self.rsc_id = data['rsc_id']
        """
        The ID of this resource.
        :type: int
        """

    # ------------------------------------------------------------------------------------------------------------------
    def get_name(self) -> str:
        """
        Returns the name of this resource.
        """
        return self.name

    # ------------------------------------------------------------------------------------------------------------------
    def get_rsc_id(self) -> str:
        """
        Returns the ID of this resource.
        """
        return self.rsc_id

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def acquire(self, *args) -> bool:
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def inquire(self, *args) -> bool:
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def release(self, *args) -> None:
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def sync_state(self):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def get_type(self):
        raise NotImplementedError()


# ----------------------------------------------------------------------------------------------------------------------
