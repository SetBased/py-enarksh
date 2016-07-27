from pystratum.mysql.StaticDataLayer import StaticDataLayer


class DataLayer(StaticDataLayer):

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_clean(p_sch_id, p_srv_id, p_run_id):
        return StaticDataLayer.execute_sp_log("call enk_back_clean(%s, %s, %s)", p_sch_id, p_srv_id, p_run_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_controller_init():
        return StaticDataLayer.execute_sp_none("call enk_back_controller_init()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_counting_resource_update_consumpted(p_rsc_id, p_rsc_amount_consumpted):
        return StaticDataLayer.execute_sp_none("call enk_back_counting_resource_update_consumpted(%s, %s)", p_rsc_id, p_rsc_amount_consumpted)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_get_host_resources():
        return StaticDataLayer.execute_sp_rows("call enk_back_get_host_resources()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_get_user_info(p_usr_login):
        return StaticDataLayer.execute_sp_row1("call enk_back_get_user_info(%s)", p_usr_login)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_node_dynamic_add_dependencies(p_nod_id_outer_worker, p_nod_id_inner_worker):
        return StaticDataLayer.execute_sp_none("call enk_back_node_dynamic_add_dependencies(%s, %s)", p_nod_id_outer_worker, p_nod_id_inner_worker)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_node_get_sch_id_by_nod_id(p_nod_id):
        return StaticDataLayer.execute_sp_singleton0("call enk_back_node_get_sch_id_by_nod_id(%s)", p_nod_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_read_write_lock_resource_update_consumpted(p_rsc_id, p_rws_id_consumpted):
        return StaticDataLayer.execute_sp_none("call enk_back_read_write_lock_resource_update_consumpted(%s, %s)", p_rsc_id, p_rws_id_consumpted)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_get_consumptions(p_run_id):
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
    def enk_back_run_node_get_dynamic_info_by_generator(p_rnd_id_generator):
        return StaticDataLayer.execute_sp_row1("call enk_back_run_node_get_dynamic_info_by_generator(%s)", p_rnd_id_generator)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_node_renew(p_rnd_id):
        return StaticDataLayer.execute_sp_singleton1("call enk_back_run_node_renew(%s)", p_rnd_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_node_update_err(p_rnd_id, p_blb_id, p_rnd_size_err):
        return StaticDataLayer.execute_sp_none("call enk_back_run_node_update_err(%s, %s, %s)", p_rnd_id, p_blb_id, p_rnd_size_err)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_node_update_log(p_rnd_id, p_blb_id, p_rnd_size_log):
        return StaticDataLayer.execute_sp_none("call enk_back_run_node_update_log(%s, %s, %s)", p_rnd_id, p_blb_id, p_rnd_size_log)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_node_update_status(p_rnd_id, p_rst_id, p_rnd_datetime_start, p_rnd_datetime_stop, p_rnd_exit_status):
        return StaticDataLayer.execute_sp_none("call enk_back_run_node_update_status(%s, %s, %s, %s, %s)", p_rnd_id, p_rst_id, p_rnd_datetime_start, p_rnd_datetime_stop, p_rnd_exit_status)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_run_update_status(p_run_id, p_run_datetime_start, p_run_datetime_stop):
        return StaticDataLayer.execute_sp_none("call enk_back_run_update_status(%s, %s, %s)", p_run_id, p_run_datetime_start, p_run_datetime_stop)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_schedule_get_current_xml(p_sch_id):
        return StaticDataLayer.execute_sp_singleton1("call enk_back_schedule_get_current_xml(%s)", p_sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_schedule_get_schedule(p_sch_id):
        return StaticDataLayer.execute_sp_row1("call enk_back_schedule_get_schedule(%s)", p_sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_schedule_revision_create_run(p_srv_id):
        return StaticDataLayer.execute_sp_singleton1("call enk_back_schedule_revision_create_run(%s)", p_srv_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_back_schedule_trigger(p_sch_id):
        return StaticDataLayer.execute_sp_singleton1("call enk_back_schedule_trigger(%s)", p_sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_blob_get_blob(p_blb_id):
        return StaticDataLayer.execute_sp_row1("call enk_blob_get_blob(%s)", p_blb_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_blob_get_details(p_blb_id):
        return StaticDataLayer.execute_sp_row1("call enk_blob_get_details(%s)", p_blb_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_blob_insert_blob(p_filename, p_mime_type, p_data):
        return StaticDataLayer.execute_sp_singleton1("call enk_blob_insert_blob(%s, %s, %s)", p_filename, p_mime_type, p_data)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_get_addendum(p_run_id):
        return StaticDataLayer.execute_sp_row1("call enk_front_run_get_addendum(%s)", p_run_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_get_all_dependencies(p_srv_id):
        return StaticDataLayer.execute_sp_rows("call enk_front_run_get_all_dependencies(%s)", p_srv_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_get_all_ports(p_run_id):
        return StaticDataLayer.execute_sp_rows("call enk_front_run_get_all_ports(%s)", p_run_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_get_all_run_nodes(p_run_id):
        return StaticDataLayer.execute_sp_rows("call enk_front_run_get_all_run_nodes(%s)", p_run_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_node_get_consumptions(p_rnd_id):
        return StaticDataLayer.execute_sp_rows("call enk_front_run_node_get_consumptions(%s)", p_rnd_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_node_get_logs(p_rnd_id):
        return StaticDataLayer.execute_sp_rows("call enk_front_run_node_get_logs(%s)", p_rnd_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_node_get_resources(p_rnd_id):
        return StaticDataLayer.execute_sp_rows("call enk_front_run_node_get_resources(%s)", p_rnd_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_node_get_status(p_rnd_id):
        return StaticDataLayer.execute_sp_row1("call enk_front_run_node_get_status(%s)", p_rnd_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_run_node_get_status_change(p_run_id, p_nsc_id):
        return StaticDataLayer.execute_sp_rows("call enk_front_run_node_get_status_change(%s, %s)", p_run_id, p_nsc_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_schedule_get_all():
        return StaticDataLayer.execute_sp_rows("call enk_front_schedule_get_all()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_front_schedule_get_all_runs(p_sch_id):
        return StaticDataLayer.execute_sp_rows("call enk_front_schedule_get_all_runs(%s)", p_sch_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_misc_insert_uri(p_uri_uri):
        return StaticDataLayer.execute_sp_singleton1("call enk_misc_insert_uri(%s)", p_uri_uri)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_consumption_store_counting_consumption(p_nod_id, p_rsc_id, p_uri_id, p_cns_amount):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_consumption_store_counting_consumption(%s, %s, %s, %s)", p_nod_id, p_rsc_id, p_uri_id, p_cns_amount)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_consumption_store_read_write_lock_consumption(p_nod_id, p_rsc_id, p_rws_id, p_uri_id):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_consumption_store_read_write_lock_consumption(%s, %s, %s, %s)", p_nod_id, p_rsc_id, p_rws_id, p_uri_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_dependency_store_dependency(p_prt_id_dependant, p_prt_id_predecessor):
        return StaticDataLayer.execute_sp_none("call enk_reader_dependency_store_dependency(%s, %s)", p_prt_id_dependant, p_prt_id_predecessor)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_host_load_host(p_hst_name):
        return StaticDataLayer.execute_sp_row1("call enk_reader_host_load_host(%s)", p_hst_name)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_host_load_resources(p_hst_id):
        return StaticDataLayer.execute_sp_rows("call enk_reader_host_load_resources(%s)", p_hst_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_host_store_host(p_hst_name):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_host_store_host(%s)", p_hst_name)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_command_job(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_user_name, p_nod_command, p_nod_master):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_command_job(%s, %s, %s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_user_name, p_nod_command, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_compound_job(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_compound_job(%s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_dynamic_inner_worker(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_dynamic_inner_worker(%s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_dynamic_job(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_dynamic_job(%s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_dynamic_outer_worker(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_dynamic_outer_worker(%s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_manual_trigger(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_manual_trigger(%s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_schedule(p_srv_id, p_uri_id, p_nod_name, p_nod_master):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_schedule(%s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_name, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_schedule_addendum(p_srv_id, p_nod_id_activate, p_nod_id_arrest, p_nod_id_schedule):
        return StaticDataLayer.execute_sp_none("call enk_reader_node_store_schedule_addendum(%s, %s, %s, %s)", p_srv_id, p_nod_id_activate, p_nod_id_arrest, p_nod_id_schedule)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_node_store_terminator(p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_node_store_terminator(%s, %s, %s, %s, %s, %s, %s)", p_srv_id, p_uri_id, p_nod_id_parent, p_nod_name, p_nod_recursion_level, p_nod_dependency_level, p_nod_master)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_port_store_input_port(p_nod_id, p_uri_id, p_prt_name):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_port_store_input_port(%s, %s, %s)", p_nod_id, p_uri_id, p_prt_name)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_port_store_output_port(p_nod_id, p_uri_id, p_prt_name):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_port_store_output_port(%s, %s, %s)", p_nod_id, p_uri_id, p_prt_name)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_resource_load_resource(p_rsc_id):
        return StaticDataLayer.execute_sp_row1("call enk_reader_resource_load_resource(%s)", p_rsc_id)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_resource_store_counting_resource(p_hst_id, p_nod_id, p_uri_id, p_rsc_name, p_rsc_amount):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_resource_store_counting_resource(%s, %s, %s, %s, %s)", p_hst_id, p_nod_id, p_uri_id, p_rsc_name, p_rsc_amount)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_resource_store_read_write_lock_resource(p_hst_id, p_nod_id, p_uri_id, p_rsc_name):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_resource_store_read_write_lock_resource(%s, %s, %s, %s)", p_hst_id, p_nod_id, p_uri_id, p_rsc_name)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def enk_reader_schedule_create_revision(p_blb_id, p_node_name):
        return StaticDataLayer.execute_sp_singleton1("call enk_reader_schedule_create_revision(%s, %s)", p_blb_id, p_node_name)


# ----------------------------------------------------------------------------------------------------------------------
