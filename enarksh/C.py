"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import os


class C:
    """
    Namespace for constants.
    """
    HOME = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

    ENARKSH_CFG = os.path.join(HOME, 'etc/enarksh.cfg')
    CREDENTIALS_CFG = os.path.join(HOME, 'etc/credentials.cfg')

    CHUNK_SIZE = 1024 * 1024

    ENK_ACT_ID_TRIGGER = 1
    ENK_ACT_ID_RESTART = 2
    ENK_ACT_ID_RESTART_FAILED = 3

    # PyStratum
    ENK_CTP_ID_COUNTING = 1
    ENK_CTP_ID_READ_WRITE = 2
    ENK_ERR_ID_NOT_CURRENT_RUN = 4
    ENK_ERR_ID_NOT_SCHEDULE_TRIGGER = 5
    ENK_ERR_ID_OK = 1
    ENK_ERR_ID_SCHEDULE_NOT_EXISTS = 2
    ENK_ERR_ID_SCHEDULE_RUNNING = 3
    ENK_NTP_COMMAND_JOB = 2
    ENK_NTP_COMPOUND_JOB = 3
    ENK_NTP_DYNAMIC_INNER_WORKER = 8
    ENK_NTP_DYNAMIC_JOB = 6
    ENK_NTP_DYNAMIC_OUTER_WORKER = 7
    ENK_NTP_MANUAL_TRIGGER = 4
    ENK_NTP_SCHEDULE = 1
    ENK_NTP_TERMINATOR = 5
    ENK_PTT_ID_INPUT = 1
    ENK_PTT_ID_OUTPUT = 2
    ENK_RST_ID_COMPLETED = 3
    ENK_RST_ID_ERROR = 4
    ENK_RST_ID_QUEUED = 5
    ENK_RST_ID_RUNNING = 2
    ENK_RST_ID_WAITING = 1
    ENK_RTP_ID_COUNTING = 1
    ENK_RTP_ID_READ_WRITE = 2
    ENK_RWS_ID_NONE = 1
    ENK_RWS_ID_READ = 2
    ENK_RWS_ID_WRITE = 3
