"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import abc


class Consumption(metaclass=abc.ABCMeta):
    """
    Consumption of a node.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, data, host_resources, schedule_resources):
        """
        Object constructor.

        :param dict data:
        :param dict host_resources:
        :param dict schedule_resources:
        """

        self.cns_id = data['cns_id']
        """
        The ID of this consumption.

        :type: int
        """

        self._resource = None
        """
        The resource from which this consumption is consuming.

        :type: Resource
        """
        if data['rsc_id'] in host_resources:
            self._resource = host_resources[data['rsc_id']]
        elif data['rsc_id'] in schedule_resources:
            self._resource = schedule_resources[data['rsc_id']]
        else:
            raise Exception("Unexpected rsc_id '%s'.", data['rsc_id'])

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def acquire_resource(self):
        """
        Actually acquires this consumption from the resource of this consumption.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def inquire_resource(self):
        """
        Returns true when there is enough resource available for this consumption. Returns false otherwise.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def release_resource(self):
        """
        Releases this consumption from the resource of this consumption.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
