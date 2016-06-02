from lib.enarksh.DataLayer import DataLayer
from lib.enarksh.XmlReader.Resource.Resource import Resource


# ----------------------------------------------------------------------------------------------------------------------
class ReadWriteLockResource(Resource):
    # ------------------------------------------------------------------------------------------------------------------
    def get_type(self) -> str:
        """
        Return the name of the type this resource type.
        """
        return 'ReadWriteLockResource'

    # ------------------------------------------------------------------------------------------------------------------
    def load_db(self, rsc_id):
        details = DataLayer.enk_reader_resource_load_resource(rsc_id)

        self._rsc_id = rsc_id
        self._resource_name = str(details['rsc_name'], 'utf8')  # XXX DL issue

    # ------------------------------------------------------------------------------------------------------------------
    def store(self, hst_id: int, nod_id: int) -> None:
        uri_id = DataLayer.enk_misc_insert_uri(self.get_uri())

        self._rsc_id = DataLayer.enk_reader_resource_store_read_write_lock_resource(hst_id,
                                                                                    nod_id,
                                                                                    uri_id,
                                                                                    self._resource_name)

# ----------------------------------------------------------------------------------------------------------------------
