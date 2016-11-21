from pystratum_mysql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class DataLayer(StaticDataLayer):
    """
    The stored routines wrappers.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_clean(p_sch_id, p_srv_id, p_run_id):
        """
        Cleans obsolete data from the database.

        :param int p_sch_id: 
                             smallint(5) unsigned
        :param int p_srv_id: 
                             smallint(5) unsigned
        :param int p_run_id: 
                             int(10) unsigned

        :rtype: int
        """
        return StaticDataLayer.execute_sp_log("call enk_back_clean(%s, %s, %s)", p_sch_id, p_srv_id, p_run_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_controller_init():
        """
        Sets the database in a predictable state. Must be called by the controller when the controller starts.

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call enk_back_controller_init()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_counting_resource_update_consumpted(p_rsc_id, p_rsc_amount_consumpted):
        """
        Updates the amount consumpted of a counting resource.

        :param int p_rsc_id: The ID of the counting resource.
                             int(11)
        :param int p_rsc_amount_consumpted: The amount consumpted.
                                            bigint(20)

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call enk_back_counting_resource_update_consumpted(%s, %s)", p_rsc_id, p_rsc_amount_consumpted)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_get_host_resources():
        """
        Selects all host resources.

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call enk_back_get_host_resources()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_get_operators():
        """
        Selects all operators (with email addresses).

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call enk_back_get_operators()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_node_dynamic_add_dependencies(p_nod_id_outer_worker, p_nod_id_inner_worker):
        """

        :param int p_nod_id_outer_worker: 
                                          int(10) unsigned
        :param int p_nod_id_inner_worker: 
                                          int(10) unsigned

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call enk_back_node_dynamic_add_dependencies(%s, %s)", p_nod_id_outer_worker, p_nod_id_inner_worker)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_node_get_sch_id_by_nod_id(p_nod_id):
        """
        Selects the ID of a schedule of node.

        :param int p_nod_id: The ID of a node.
                             int(10) unsigned

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton0("call enk_back_node_get_sch_id_by_nod_id(%s)", p_nod_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_read_write_lock_resource_update_consumpted(p_rsc_id, p_rws_id_consumpted):
        """
        Updates the RW lock status of a RW lock resource.

        :param int p_rsc_id: The ID of the RW resource.
                             int(11)
        :param int p_rws_id_consumpted: The ID of the consumption.
                                        tinyint(3) unsigned

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call enk_back_read_write_lock_resource_update_consumpted(%s, %s)", p_rsc_id, p_rws_id_consumpted)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_get_consumptions(p_run_id):
        """
        Selects all consumptions of all nodes of schedule revision.

        :param int p_run_id: 
                             int(10) unsigned

        :rtype: dict
        """
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call enk_back_run_get_consumptions(%s)", p_run_id)
        for row in rows:
            if row['rnd_id'] in ret:
                ret[row['rnd_id']].append(row)
            else:
                ret[row['rnd_id']] = [row]

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_get_dependants(p_srv_id):
        """
        Selects all dependants of all ports of all nodes of a schedule revision.

        :param int p_srv_id: The Id of the schedule revision.
                             smallint(5) unsigned

        :rtype: dict
        """
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call enk_back_run_get_dependants(%s)", p_srv_id)
        for row in rows:
            if row['prt_id_predecessor'] in ret:
                ret[row['prt_id_predecessor']].append(row)
            else:
                ret[row['prt_id_predecessor']] = [row]

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_get_dependencies(p_srv_id):
        """
        Selects all dependencies of all ports of all nodes of a schedule revision.

        :param int p_srv_id: The Id of the schedule revision.
                             smallint(5) unsigned

        :rtype: dict
        """
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call enk_back_run_get_dependencies(%s)", p_srv_id)
        for row in rows:
            if row['prt_id_dependant'] in ret:
                ret[row['prt_id_dependant']].append(row)
            else:
                ret[row['prt_id_dependant']] = [row]

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_get_ports1(p_run_id):
        """
        Selects all ports of all nodes in a schedule revision.

        :param int p_run_id: The ID of the run.
                             int(10) unsigned

        :rtype: dict
        """
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call enk_back_run_get_ports1(%s)", p_run_id)
        for row in rows:
            if row['prt_id'] in ret:
                raise Exception('Duplicate key for %s.' % str((row['prt_id'])))
            else:
                ret[row['prt_id']] = row

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_get_ports2(p_run_id):
        """
        Selects all ports of all nodes in a schedule revision.

        :param int p_run_id: The ID of the run.
                             int(10) unsigned

        :rtype: dict
        """
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call enk_back_run_get_ports2(%s)", p_run_id)
        for row in rows:
            if row['rnd_id'] in ret:
                ret[row['rnd_id']].append(row)
            else:
                ret[row['rnd_id']] = [row]

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_get_resources(p_run_id):
        """
        Selects all resources of all nodes in a schedule revision.

        :param int p_run_id: The ID of the run.
                             int(10) unsigned

        :rtype: dict
        """
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call enk_back_run_get_resources(%s)", p_run_id)
        for row in rows:
            if row['rnd_id'] in ret:
                ret[row['rnd_id']].append(row)
            else:
                ret[row['rnd_id']] = [row]

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_get_run_nodes(p_run_id):
        """
        Selects all current nodes in a schedule revision.

        :param int p_run_id: The ID of the run.
                             int(10) unsigned

        :rtype: dict
        """
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call enk_back_run_get_run_nodes(%s)", p_run_id)
        for row in rows:
            if row['rnd_id'] in ret:
                raise Exception('Duplicate key for %s.' % str((row['rnd_id'])))
            else:
                ret[row['rnd_id']] = row

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_node_find_by_uri(p_uri_uri):
        """
        Selects a current run node based on the URI of the node.

        :param str p_uri_uri: The URI of the node.
                              varchar(4000) character set ascii collation ascii_general_ci

        :rtype: None|dict[str,*]
        """
        return StaticDataLayer.execute_sp_row0("call enk_back_run_node_find_by_uri(%s)", p_uri_uri)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_node_get_details(p_rnd_id):
        """
        Selects the details of a run node.

        :param int p_rnd_id: The ID of the run node.
                             int(11)

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call enk_back_run_node_get_details(%s)", p_rnd_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_node_get_dynamic_info_by_generator(p_rnd_id_generator):
        """
        Selects data of a dynamic node by the node ID of its generator.

        :param int p_rnd_id_generator: The run node ID of the generator.
                                       int(11)

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call enk_back_run_node_get_dynamic_info_by_generator(%s)", p_rnd_id_generator)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_node_renew(p_rnd_id):
        """
        xxx

        :param int p_rnd_id: 
                             int(11)

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_back_run_node_renew(%s)", p_rnd_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_node_update_err(p_rnd_id, p_blb_id, p_rnd_size_err):
        """
        Updates a node with metadata about the STDERR log.

        :param int p_rnd_id: The ID of the run node.
                             int(11)
        :param int p_blb_id: The ID of the BLOB with the log.
                             int(10) unsigned
        :param int p_rnd_size_err: The total log size.
                                   bigint(20) unsigned

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call enk_back_run_node_update_err(%s, %s, %s)", p_rnd_id, p_blb_id, p_rnd_size_err)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_node_update_log(p_rnd_id, p_blb_id, p_rnd_size_log):
        """
        Updates a node with metadata about the STDOUT.

        :param int p_rnd_id: The ID of the run node.
                             int(11)
        :param int p_blb_id: The ID of the BLOB with the log.
                             int(10) unsigned
        :param int p_rnd_size_log: The total log size.
                                   bigint(20) unsigned

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call enk_back_run_node_update_log(%s, %s, %s)", p_rnd_id, p_blb_id, p_rnd_size_log)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_node_update_status(p_rnd_id, p_rst_id, p_rnd_datetime_start, p_rnd_datetime_stop, p_rnd_exit_status):
        """
        Marks node @a p_rnd_id as stopped with status @a p_rst_id.

        :param int p_rnd_id: 
                             int(11)
        :param int p_rst_id: 
                             tinyint(3) unsigned
        :param str p_rnd_datetime_start: 
                                         datetime
        :param str p_rnd_datetime_stop: 
                                        datetime
        :param int p_rnd_exit_status: 
                                      int(11)

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call enk_back_run_node_update_status(%s, %s, %s, %s, %s)", p_rnd_id, p_rst_id, p_rnd_datetime_start, p_rnd_datetime_stop, p_rnd_exit_status)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_update_status(p_run_id, p_run_datetime_start, p_run_datetime_stop):
        """
        Update the status of a run.

        :param int p_run_id: The ID of the run.
                             int(10) unsigned
        :param str p_run_datetime_start: The start datetime of the run.
                                         datetime
        :param str p_run_datetime_stop: The stop datetime of the run.
                                        datetime

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call enk_back_run_update_status(%s, %s, %s)", p_run_id, p_run_datetime_start, p_run_datetime_stop)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_schedule_delete(p_sch_id):
        """
        Deletes an entire schedule.

        :param int p_sch_id: 
                             smallint(5) unsigned

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call enk_back_schedule_delete(%s)", p_sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_schedule_get_current_xml(p_sch_id):
        """
        Selects the XML definition of the current version of a schedule.

        :param int p_sch_id: The ID of the schedule.
                             smallint(5) unsigned

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_back_schedule_get_current_xml(%s)", p_sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_schedule_get_schedule(p_sch_id):
        """
        Selects data of a schedule.

        :param int p_sch_id: The ID of the schedule.
                             smallint(5) unsigned

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call enk_back_schedule_get_schedule(%s)", p_sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_schedule_revision_create_run(p_srv_id):
        """
        Creates a new run for schedule revision p_srv_id.

        :param int p_srv_id: 
                             smallint(5) unsigned

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_back_schedule_revision_create_run(%s)", p_srv_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_schedule_trigger(p_sch_id):
        """
        Triggers a schedule.

        :param int p_sch_id: 
                             smallint(5) unsigned

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_back_schedule_trigger(%s)", p_sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_blob_get_blob(p_blb_id):
        """
        Selects the data of a BLOB.

        :param int p_blb_id: The ID of the BLOB.
                             int(10) unsigned

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call enk_blob_get_blob(%s)", p_blb_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_blob_get_details(p_blb_id):
        """
        Selects the details of a BLOB (but not the data).

        :param int p_blb_id: The ID of the BLOB.
                             int(10) unsigned

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call enk_blob_get_details(%s)", p_blb_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_blob_insert_blob(p_filename, p_mime_type, p_data):
        """
        Inserts a BLOB and selects the ID of the BLOB.

        :param str p_filename: The filename associated with the BLOB.
                               varchar(255) character set utf8 collation utf8_general_ci
        :param str p_mime_type: The mime type of the data.
                                varchar(48) character set utf8 collation utf8_general_ci
        :param bytes p_data: The data of the BLOB.
                             longblob

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_blob_insert_blob(%s, %s, %s)", p_filename, p_mime_type, p_data)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_get_addendum(p_run_id):
        """
        Selects the addendum of a schedule revision of a run.

        :param int p_run_id: The ID of the run.
                             int(10) unsigned

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call enk_front_run_get_addendum(%s)", p_run_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_get_all_dependencies(p_srv_id):
        """
        Selects all dependencies of all ports of all nodes of a schedule revision.

        :param int p_srv_id: The ID of the schedule revision.
                             smallint(5) unsigned

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call enk_front_run_get_all_dependencies(%s)", p_srv_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_get_all_ports(p_run_id):
        """
        Selects all ports of all nodes of a run.

        :param int p_run_id: The ID of the run
                             int(10) unsigned

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call enk_front_run_get_all_ports(%s)", p_run_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_get_all_run_nodes(p_run_id):
        """
        Selects all nodes of a a run.

        :param int p_run_id: The ID of the run.
                             int(10) unsigned

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call enk_front_run_get_all_run_nodes(%s)", p_run_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_node_get_consumptions(p_rnd_id):
        """
        Selects all consumptions of a run node.

        :param int p_rnd_id: 
                             int(11)

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call enk_front_run_node_get_consumptions(%s)", p_rnd_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_node_get_logs(p_rnd_id):
        """
        Selects all logs of a run node.

        :param int p_rnd_id: 
                             int(11)

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call enk_front_run_node_get_logs(%s)", p_rnd_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_node_get_resources(p_rnd_id):
        """
        Selects all resources of a node.

        :param int p_rnd_id: The ID of the node.
                             int(11)

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call enk_front_run_node_get_resources(%s)", p_rnd_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_node_get_status(p_rnd_id):
        """
        Selects current status of a run node.

        :param int p_rnd_id: The ID of the run node.
                             int(11)

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call enk_front_run_node_get_status(%s)", p_rnd_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_node_get_status_change(p_run_id, p_nsc_id):
        """
        Selects all node status changes of a run after a run node status change.

        :param int p_run_id: The ID of the run.
                             int(10) unsigned
        :param int p_nsc_id: The ID of the node status change.
                             int(10) unsigned

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call enk_front_run_node_get_status_change(%s, %s)", p_run_id, p_nsc_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_schedule_get_all():
        """
        Selects all schedules.

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call enk_front_schedule_get_all()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_schedule_get_all_runs(p_sch_id):
        """
        Selects all runs of a schedule.

        :param int p_sch_id: The ID of the schedule.
                             smallint(5) unsigned

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call enk_front_schedule_get_all_runs(%s)", p_sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_misc_insert_uri(p_uri_uri):
        """
        Selects the ID of an URI. If the URI doesn't exists it will be inserted.

        :param str p_uri_uri: The URI.
                              varchar(4000) character set ascii collation ascii_general_ci

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_misc_insert_uri(%s)", p_uri_uri)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_consumption_store_counting_consumption(p_nod_id, p_rsc_id, p_uri_id, p_cns_amount):
        """
        Stores a consumption of type "ReadWriteLockConsumption" and selects the @c cns_id of the new consumption.

        :param int p_nod_id: The ID of the node of that will make consumption.
                             int(10) unsigned
        :param int p_rsc_id: The ID of the resource that will be consumpted.
                             int(11)
        :param int p_uri_id: The ID of the URI of the consumption.
                             int(10) unsigned
        :param int p_cns_amount: The amount that will be consumpted.
                                 bigint(20)

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_consumption_store_counting_consumption(%s, %s, %s, %s)", p_nod_id, p_rsc_id, p_uri_id, p_cns_amount)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_consumption_store_read_write_lock_consumption(p_nod_id, p_rsc_id, p_rws_id, p_uri_id):
        """
        Stores a consumption of type "ReadWriteLockConsumption" and selects the ID of the new consumption.

        :param int p_nod_id: The ID of the node that will make consumption.
                             int(10) unsigned
        :param int p_rsc_id: The ID of the resource that will be consumpted.
                             int(11)
        :param int p_rws_id: The RW status of the consumption.
                             tinyint(3) unsigned
        :param int p_uri_id: The ID of the URI of the consumption.
                             int(10) unsigned

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_consumption_store_read_write_lock_consumption(%s, %s, %s, %s)", p_nod_id, p_rsc_id, p_rws_id, p_uri_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_dependency_store_dependency(p_prt_id_dependant, p_prt_id_predecessor):
        """
        Stores a dependency between two ports.

        :param int p_prt_id_dependant: The ID of the dependant port
                                       int(10) unsigned
        :param int p_prt_id_predecessor: The ID of the predecessor port.
                                         int(10) unsigned

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call enk_reader_dependency_store_dependency(%s, %s)", p_prt_id_dependant, p_prt_id_predecessor)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_host_load_host(p_hst_name):
        """
        Selects the details of a host.

        :param str p_hst_name: The hostname.
                               varchar(64) character set utf8 collation utf8_general_ci

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call enk_reader_host_load_host(%s)", p_hst_name)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_host_load_resources(p_hst_id):
        """
        Selects the resources of a host.

        :param int p_hst_id: The ID of the host.
                             smallint(5) unsigned

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call enk_reader_host_load_resources(%s)", p_hst_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_host_store_host(p_hst_name):
        """
        Stores a host and selects the IF of the host.

        :param str p_hst_name: The hostname.
                               varchar(64) character set utf8 collation utf8_general_ci

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_host_store_host(%s)", p_hst_name)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_command_job(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_user_name, p_nod_command, p_nod_master):
        """
        Stores a node of type "command job" and selects the ID of the new node.

        :param int p_srv_id: The ID of the schedule revision.
                             smallint(5) unsigned
        :param int p_uri_id: The ID of the URI of the node.
                             int(10) unsigned
        :param int p_nod_id_parent: The ID of parent node of the node.
                                    int(10) unsigned
        :param str p_nod_name: The name of the node.
                               varchar(64) character set ascii collation ascii_general_ci
        :param int p_nod_recursion_level: The recursion level (i.e. the number of parents).
                                          int(11)
        :param int p_nod_dependency_level: The dependency level (i.e. the number of dependencies from the parent input ports).
                                           int(11)
        :param str p_nod_user_name: The account under which the command must run.
                                    varchar(32) character set utf8 collation utf8_general_ci
        :param str p_nod_command: The command that must be executed (serialized array).
                                  varchar(1000) character set utf8 collation utf8_general_ci
        :param int p_nod_master: 
                                 tinyint(1)

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_command_job(%s, %s, %s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_user_name, p_nod_command, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_compound_job(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master):
        """
        Stores a node of type "compound job" and selects the ID of the new node.

        :param int p_srv_id: The ID of the schedule revision.
                             smallint(5) unsigned
        :param int p_uri_id: The ID of the URI of the node.
                             int(10) unsigned
        :param int p_nod_id_parent: The ID of parent node of the node.
                                    int(10) unsigned
        :param str p_nod_name: The name of the node.
                               varchar(64) character set ascii collation ascii_general_ci
        :param int p_nod_recursion_level: The recursion level (i.e. the number of parents).
                                          int(11)
        :param int p_nod_dependency_level: The dependency level (i.e. the number of dependencies from the parent input ports).
                                           int(11)
        :param int p_nod_master: 
                                 tinyint(1)

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_compound_job(%s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_dynamic_inner_worker(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master):
        """
        Stores a node of type "dynamic inner worker" and selects the ID of the new node.

        :param int p_srv_id: The ID of the schedule revision.
                             smallint(5) unsigned
        :param int p_uri_id: The ID of the URI of the node.
                             int(10) unsigned
        :param int p_nod_id_parent: The ID of parent node of the node.
                                    int(10) unsigned
        :param str p_nod_name: The name of the node.
                               varchar(64) character set ascii collation ascii_general_ci
        :param int p_nod_recursion_level: The recursion level (i.e. the number of parents).
                                          int(11)
        :param int p_nod_dependency_level: The dependency level (i.e. the number of dependencies from the parent input ports).
                                           int(11)
        :param int p_nod_master: 
                                 tinyint(1)

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_dynamic_inner_worker(%s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_dynamic_job(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master):
        """
        Stores a node of type "dynamic job" and selects the ID of the new node.

        :param int p_srv_id: The ID of the schedule revision.
                             smallint(5) unsigned
        :param int p_uri_id: The ID of the URI of the node.
                             int(10) unsigned
        :param int p_nod_id_parent: The ID of parent node of the node.
                                    int(10) unsigned
        :param str p_nod_name: The name of the node.
                               varchar(64) character set ascii collation ascii_general_ci
        :param int p_nod_recursion_level: The recursion level (i.e. the number of parents).
                                          int(11)
        :param int p_nod_dependency_level: The dependency level (i.e. the number of dependencies from the parent input ports).
                                           int(11)
        :param int p_nod_master: 
                                 tinyint(1)

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_dynamic_job(%s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_dynamic_outer_worker(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master):
        """
        Stores a node of type "dynamic outer worker" and selects the ID of the new node.

        :param int p_srv_id: The ID of the schedule revision.
                             smallint(5) unsigned
        :param int p_uri_id: The ID of the URI of the node.
                             int(10) unsigned
        :param int p_nod_id_parent: The ID of parent node of the node.
                                    int(10) unsigned
        :param str p_nod_name: The name of the node.
                               varchar(64) character set ascii collation ascii_general_ci
        :param int p_nod_recursion_level: The recursion level (i.e. the number of parents).
                                          int(11)
        :param int p_nod_dependency_level: The dependency level (i.e. the number of dependencies from the parent input ports).
                                           int(11)
        :param int p_nod_master: 
                                 tinyint(1)

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_dynamic_outer_worker(%s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_manual_trigger(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master):
        """
        Stores a node of type "manual trigger" and selects the ID of the new node.

        :param int p_srv_id: The ID of the schedule revision.
                             smallint(5) unsigned
        :param int p_uri_id: The ID of the URI of the node.
                             int(10) unsigned
        :param int p_nod_id_parent: The ID of parent node of the node.
                                    int(10) unsigned
        :param str p_nod_name: The name of the node.
                               varchar(64) character set ascii collation ascii_general_ci
        :param int p_nod_recursion_level: The recursion level (i.e. the number of parents).
                                          int(11)
        :param int p_nod_dependency_level: The dependency level (i.e. the number of dependencies from the parent input ports).
                                           int(11)
        :param int p_nod_master: 
                                 tinyint(1)

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_manual_trigger(%s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_schedule(p_srv_id, p_uri_id, p_nod_name, p_nod_master):
        """
        Stores a node of type "schedule" and selects the ID of the new node.

        :param int p_srv_id: The ID of the schedule revision.
                             smallint(5) unsigned
        :param int p_uri_id: The ID of the URI of the node.
                             int(10) unsigned
        :param str p_nod_name: The name of the node.
                               varchar(64) character set ascii collation ascii_general_ci
        :param int p_nod_master: 
                                 tinyint(1)

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_schedule(%s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_name, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_schedule_addendum(p_srv_id, p_nod_id_activate, p_nod_id_arrest, p_nod_id_schedule):
        """
        Stores additional information of a schedule revision and selects the ID of the new node.

        :param int p_srv_id: The ID of the schedule revision.
                             smallint(5) unsigned
        :param int p_nod_id_activate: The ID of the activate node of the schedule.
                                      int(10) unsigned
        :param int p_nod_id_arrest: The ID of the arrest node of the schedule.
                                    int(10) unsigned
        :param int p_nod_id_schedule: The ID of the schedule node it self.
                                      int(10) unsigned

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call enk_reader_node_store_schedule_addendum(%s, %s, %s, %s)", p_srv_id, p_nod_id_activate, p_nod_id_arrest, p_nod_id_schedule)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_terminator(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master):
        """
        Stores a node of type "terminator" and selects the ID of the new node.

        :param int p_srv_id: The ID of the schedule revision.
                             smallint(5) unsigned
        :param int p_uri_id: The ID of the URI of the node.
                             int(10) unsigned
        :param int p_nod_id_parent: The ID of parent node of the node.
                                    int(10) unsigned
        :param str p_nod_name: The name of the node.
                               varchar(64) character set ascii collation ascii_general_ci
        :param int p_nod_recursion_level: The recursion level (i.e. the number of parents).
                                          int(11)
        :param int p_nod_dependency_level: The dependency level (i.e. the number of dependencies from the parent input ports).
                                           int(11)
        :param int p_nod_master: 
                                 tinyint(1)

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_terminator(%s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_port_store_input_port(p_nod_id, p_uri_id, p_prt_name):
        """
        Stores a port of type "InputPort" and selects the ID of the new port.

        :param int p_nod_id: The ID of the node of the node of the input port.
                             int(10) unsigned
        :param int p_uri_id: The ID of the URI of the input port.
                             int(10) unsigned
        :param str p_prt_name: The name of the input port.
                               varchar(64) character set ascii collation ascii_general_ci

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_port_store_input_port(%s, %s, %s)", p_nod_id, p_uri_id, p_prt_name)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_port_store_output_port(p_nod_id, p_uri_id, p_prt_name):
        """
        Stores a port of type "OutputPort" and selects the ID of the new port.

        :param int p_nod_id: The ID of the node of the node of the output port.
                             int(10) unsigned
        :param int p_uri_id: The ID of the URI of the output port.
                             int(10) unsigned
        :param str p_prt_name: The name of the output port.
                               varchar(64) character set ascii collation ascii_general_ci

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_port_store_output_port(%s, %s, %s)", p_nod_id, p_uri_id, p_prt_name)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_resource_load_resource(p_rsc_id):
        """
        Selects the details of a resource.

        :param int p_rsc_id: The ID of the resource.
                             int(11)

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call enk_reader_resource_load_resource(%s)", p_rsc_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_resource_store_counting_resource(p_hst_id, p_nod_id, p_uri_id, p_rsc_name, p_rsc_amount):
        """
        Stores a resource of type "CountingResource" and selects the ID of the new resource.

        :param int p_hst_id: The ID of the host of the resource.
                             smallint(5) unsigned
        :param int p_nod_id: The ID of the node of the resource.
                             int(10) unsigned
        :param int p_uri_id: The ID of the URI of the resource.
                             int(10) unsigned
        :param str p_rsc_name: The name of the resource.
                               varchar(64) character set ascii collation ascii_general_ci
        :param int p_rsc_amount: The total available amount of this resource.
                                 bigint(20)

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_resource_store_counting_resource(%s, %s, %s, %s, %s)", p_hst_id, p_nod_id, p_uri_id, p_rsc_name, p_rsc_amount)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_resource_store_read_write_lock_resource(p_hst_id, p_nod_id, p_uri_id, p_rsc_name):
        """
        Stores a resource of type "ReadWriteLockResource" and selects the ID of the new resource.

        :param int p_hst_id: The ID of the host of the resource.
                             smallint(5) unsigned
        :param int p_nod_id: The ID of the node of the resource.
                             int(10) unsigned
        :param int p_uri_id: The ID of the URI of the resource.
                             int(10) unsigned
        :param str p_rsc_name: The name of the resource.
                               varchar(64) character set ascii collation ascii_general_ci

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_resource_store_read_write_lock_resource(%s, %s, %s, %s)", p_hst_id, p_nod_id, p_uri_id, p_rsc_name)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_schedule_create_revision(p_blb_id, p_node_name):
        """
        Stores a node of type "schedule" and selects the ID of the new schedule revision.
If the schedule revision in ID is already loaded and up-to-date NULL is selected.

        :param int p_blb_id: The ID of the blob of the XML definition of the schedule.
                             int(10) unsigned
        :param str p_node_name: The name of the schedule.
                                varchar(64) character set ascii collation ascii_general_ci

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_schedule_create_revision(%s, %s)", p_blb_id, p_node_name)


# ----------------------------------------------------------------------------------------------------------------------
