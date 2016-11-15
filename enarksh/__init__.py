import os

# ----------------------------------------------------------------------------------------------------------------------
HOME = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

CONTROLLER_PULL_END_POINT = 'tcp://127.0.0.1:7771'
CONTROLLER_LOCKSTEP_END_POINT = 'tcp://127.0.0.1:7772'
LOGGER_PULL_END_POINT = 'tcp://127.0.0.1:7773'
SPAWNER_PULL_END_POINT = 'tcp://127.0.0.1:7774'

MYSQL_HOSTNAME = '127.0.0.1'
MYSQL_USERNAME = 'enarksh_owner'
MYSQL_PASSWORD = 'cH5thast2stebeT3'
MYSQL_SCHEMA = 'enarksh'
MYSQL_PORT = 3306

CHUNK_SIZE = 1024 * 1024

ENK_RST_ID_COMPLETED = 3
ENK_RST_ID_ERROR = 4
ENK_RST_ID_QUEUED = 5
ENK_RST_ID_RUNNING = 2
ENK_RST_ID_WAITING = 1

ENK_ACT_ID_TRIGGER = 1
ENK_ACT_ID_RESTART = 2
ENK_ACT_ID_RESTART_FAILED = 3

ENK_PTT_ID_INPUT = 1
ENK_PTT_ID_OUTPUT = 2

ENK_RWS_ID_NONE = 1
ENK_RWS_ID_READ = 2
ENK_RWS_ID_WRITE = 3

ENK_RTP_ID_COUNTING = 1
ENK_RTP_ID_READ_WRITE = 2

ENK_CTP_ID_COUNTING = 1
ENK_CTP_ID_READ_WRITE = 2

ENK_NTP_SCHEDULE = 1
ENK_NTP_COMMAND_JOB = 2
ENK_NTP_COMPOUND_JOB = 3
ENK_NTP_MANUAL_TRIGGER = 4
ENK_NTP_TERMINATOR = 5
ENK_NTP_DYNAMIC_JOB = 6
ENK_NTP_DYNAMIC_OUTER_WORKER = 7
ENK_NTP_DYNAMIC_INNER_WORKER = 8

ENK_MESSAGE_ADMIN_DIR = os.path.join(HOME, 'var/lib/message/admin')
ENK_MESSAGE_CONTROLLER_DIR = os.path.join(HOME, 'var/lib/message/controller')
ENK_MESSAGE_LOGGER_DIR = os.path.join(HOME, 'var/lib/message/logger')
ENK_MESSAGE_SPAWNER_DIR = os.path.join(HOME, 'var/lib/message/spawner')
ENK_LOCK_DIR = os.path.join(HOME, 'var/lock')

# ----------------------------------------------------------------------------------------------------------------------
