from lib.enarksh.XmlReader.Resource import Resource


# ----------------------------------------------------------------------------------------------------------------------
class FakeParent:
    def __init__(self, schedule, host_resources: dict, nod_id, rnd_id):
        self._schedule = schedule
        self._host_resources = host_resources
        self._nod_id = nod_id

        self._node = schedule.get_node(rnd_id)

    # ------------------------------------------------------------------------------------------------------------------
    def get_resource_by_name(self, name: str) -> Resource:
        resource = self._node.fake_get_resource_by_name(name)
        if resource:
            return resource

        for resource in self._host_resources.values():
            if resource.get_name() == name:
                return resource

        return None

    # ------------------------------------------------------------------------------------------------------------------
    def get_uri(self, obj_type: str='node') -> str:
        return self._node.get_uri(obj_type)

# ----------------------------------------------------------------------------------------------------------------------
