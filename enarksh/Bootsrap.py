"""
Enarksh

Copyright 2013-2016 Set Based IT Consultancy

Licence MIT
"""
import os
import subprocess
import sys

from pystratum_mysql.StaticDataLayer import StaticDataLayer

import enarksh
from enarksh.DataLayer import DataLayer


class Bootstrap:
    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _drop_routines():
        """
        Drops all stored routines form the databases.
        """
        rows = DataLayer.execute_rows('select ROUTINE_TYPE routine_type '
                                      ',      ROUTINE_NAME routine_name '
                                      'from   information_schema.ROUTINES '
                                      'where  ROUTINE_SCHEMA = database() '
                                      'and    ROUTINE_TYPE   = "PROCEDURE" '
                                      'order by ROUTINE_NAME')
        for row in rows:
            print('Dropping %s %s' % (row['routine_type'], row['routine_name']))
            DataLayer.execute_none('drop %s %s' % (row['routine_type'], row['routine_name']))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _drop_views():
        """
        Drops all views form the databases.
        """
        rows = DataLayer.execute_rows('SELECT TABLE_NAME table_name '
                                      'FROM   information_schema.TABLES '
                                      'WHERE  TABLE_SCHEMA = database() '
                                      'AND    TABLE_TYPE   = "VIEW" '
                                      'ORDER BY table_name')
        for row in rows:
            print('Dropping view %s' % row['table_name'])
            DataLayer.execute_none('drop view %s' % row['table_name'])

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _drop_tables():
        """
        Drops all tables form the databases.
        """
        DataLayer.execute_none('set foreign_key_checks = off')

        rows = DataLayer.execute_rows('SELECT TABLE_NAME table_name '
                                      'FROM   information_schema.TABLES '
                                      'WHERE  TABLE_SCHEMA = database() '
                                      'AND    TABLE_TYPE   = "BASE TABLE" '
                                      'ORDER BY TABLE_NAME')
        for row in rows:
            print('Dropping table %s' % row['table_name'])
            DataLayer.execute_none('drop table %s cascade' % row['table_name'])

        DataLayer.execute_none('set foreign_key_checks = on')

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _execute_sql_file(filename, encoding=None):
        """
        Executes a statements in file.

        :param filename: The file SQL statements.
        :param encoding: The encoding of the file.
        """
        print("Executing script '%s'." % filename)

        file = open(os.path.join(enarksh.HOME, filename), 'rt', encoding=encoding)
        sql = file.read()
        file.close()

        StaticDataLayer.connection.cmd_query_iter(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_all_db_objects(self):
        """
        Drops all objects form the databases.
        """
        self._drop_tables()
        self._drop_views()
        self._drop_routines()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _load_stored_routines():
        """
        Loads a stored routines and user defined functions into the database.
        """
        # Python doesn't flush its stdout and stderr buffers before a subprocess.call (as a consequence the log of
        # the subprocess can end up anywhere in the log of this process). So, we have to flush stdout and stderr our
        # self.
        sys.stdout.flush()
        sys.stderr.flush()

        ret = subprocess.call(['pystratum', 'stratum', os.path.join(enarksh.HOME, 'etc/stratum.cfg')])
        if ret != 0:
            raise RuntimeError('Error loading stored procedures and user defined functions.')

    # ------------------------------------------------------------------------------------------------------------------
    def main(self):
        """
        Bootstrap the database for our WOB enarksh. Removes all database objects and (re)creates all databases objects.
        """
        # Set database configuration options.
        DataLayer.config['host'] = enarksh.MYSQL_HOSTNAME
        DataLayer.config['user'] = enarksh.MYSQL_USERNAME
        DataLayer.config['password'] = enarksh.MYSQL_PASSWORD
        DataLayer.config['database'] = enarksh.MYSQL_SCHEMA
        DataLayer.config['port'] = enarksh.MYSQL_PORT
        DataLayer.config['autocommit'] = False

        # Connect to the MySQL.
        DataLayer.connect()

        # Remove all databases objects.
        self._drop_all_db_objects()

        # Create all types and tables.
        self._execute_sql_file('lib/ddl/0100_create_tables.sql', 'utf-8')

        # Load static data.
        self._execute_sql_file('lib/ddl/0300_enk_consumption_type.sql')
        self._execute_sql_file('lib/ddl/0300_enk_error.sql')
        self._execute_sql_file('lib/ddl/0300_enk_host.sql')
        self._execute_sql_file('lib/ddl/0300_enk_node_type.sql')
        self._execute_sql_file('lib/ddl/0300_enk_port_type.sql')
        self._execute_sql_file('lib/ddl/0300_enk_resource_type.sql')
        self._execute_sql_file('lib/ddl/0300_enk_run_status.sql')
        self._execute_sql_file('lib/ddl/0300_enk_rw_status.sql')

        # self._execute_sql_file('lib/ddl/0500_create_views.sql')

        # Load all stored procedure and functions.
        DataLayer.commit()
        self._load_stored_routines()

# ----------------------------------------------------------------------------------------------------------------------
