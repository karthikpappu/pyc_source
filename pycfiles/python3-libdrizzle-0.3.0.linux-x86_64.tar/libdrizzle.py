# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.1/dist-packages/drizzle/libdrizzle.py
# Compiled at: 2009-10-07 15:00:49
from sys import version_info
if version_info >= (2, 6, 0):

    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_libdrizzle', [dirname(__file__)])
        except ImportError:
            import _libdrizzle
            return _libdrizzle

        if fp is not None:
            try:
                _mod = imp.load_module('_libdrizzle', fp, pathname, description)
            finally:
                fp.close()

            return _mod
        else:
            return


    _libdrizzle = swig_import_helper()
    del swig_import_helper
else:
    import _libdrizzle
del version_info
try:
    _swig_property = property
except NameError:
    pass

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if name == 'thisown':
        return self.this.own(value)
    else:
        if name == 'this':
            if type(value).__name__ == 'SwigPyObject':
                self.__dict__[name] = value
                return
        method = class_type.__swig_setmethods__.get(name, None)
        if method:
            return method(self, value)
        if not static or hasattr(self, name):
            self.__dict__[name] = value
        else:
            raise AttributeError('You cannot add attributes to %s' % self)
        return


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if name == 'thisown':
        return self.this.own()
    else:
        method = class_type.__swig_getmethods__.get(name, None)
        if method:
            return method(self)
        raise AttributeError(name)
        return


def _swig_repr(self):
    try:
        strthis = 'proxy of ' + self.this.__repr__()
    except:
        strthis = ''

    return '<%s.%s; %s >' % (self.__class__.__module__, self.__class__.__name__, strthis)


try:
    _object = object
    _newclass = 1
except AttributeError:

    class _object:
        pass


    _newclass = 0

DRIZZLE_DEFAULT_TCP_HOST = _libdrizzle.DRIZZLE_DEFAULT_TCP_HOST
DRIZZLE_DEFAULT_TCP_PORT = _libdrizzle.DRIZZLE_DEFAULT_TCP_PORT
DRIZZLE_DEFAULT_TCP_PORT_MYSQL = _libdrizzle.DRIZZLE_DEFAULT_TCP_PORT_MYSQL
DRIZZLE_DEFAULT_UDS = _libdrizzle.DRIZZLE_DEFAULT_UDS
DRIZZLE_DEFAULT_USER = _libdrizzle.DRIZZLE_DEFAULT_USER
DRIZZLE_MAX_ERROR_SIZE = _libdrizzle.DRIZZLE_MAX_ERROR_SIZE
DRIZZLE_MAX_USER_SIZE = _libdrizzle.DRIZZLE_MAX_USER_SIZE
DRIZZLE_MAX_PASSWORD_SIZE = _libdrizzle.DRIZZLE_MAX_PASSWORD_SIZE
DRIZZLE_MAX_DB_SIZE = _libdrizzle.DRIZZLE_MAX_DB_SIZE
DRIZZLE_MAX_INFO_SIZE = _libdrizzle.DRIZZLE_MAX_INFO_SIZE
DRIZZLE_MAX_SQLSTATE_SIZE = _libdrizzle.DRIZZLE_MAX_SQLSTATE_SIZE
DRIZZLE_MAX_CATALOG_SIZE = _libdrizzle.DRIZZLE_MAX_CATALOG_SIZE
DRIZZLE_MAX_TABLE_SIZE = _libdrizzle.DRIZZLE_MAX_TABLE_SIZE
DRIZZLE_MAX_COLUMN_NAME_SIZE = _libdrizzle.DRIZZLE_MAX_COLUMN_NAME_SIZE
DRIZZLE_MAX_DEFAULT_VALUE_SIZE = _libdrizzle.DRIZZLE_MAX_DEFAULT_VALUE_SIZE
DRIZZLE_MAX_BUFFER_SIZE = _libdrizzle.DRIZZLE_MAX_BUFFER_SIZE
DRIZZLE_BUFFER_COPY_THRESHOLD = _libdrizzle.DRIZZLE_BUFFER_COPY_THRESHOLD
DRIZZLE_MAX_SERVER_VERSION_SIZE = _libdrizzle.DRIZZLE_MAX_SERVER_VERSION_SIZE
DRIZZLE_MAX_SCRAMBLE_SIZE = _libdrizzle.DRIZZLE_MAX_SCRAMBLE_SIZE
DRIZZLE_STATE_STACK_SIZE = _libdrizzle.DRIZZLE_STATE_STACK_SIZE
DRIZZLE_ROW_GROW_SIZE = _libdrizzle.DRIZZLE_ROW_GROW_SIZE
DRIZZLE_DEFAULT_SOCKET_TIMEOUT = _libdrizzle.DRIZZLE_DEFAULT_SOCKET_TIMEOUT
DRIZZLE_DEFAULT_SOCKET_SEND_SIZE = _libdrizzle.DRIZZLE_DEFAULT_SOCKET_SEND_SIZE
DRIZZLE_DEFAULT_SOCKET_RECV_SIZE = _libdrizzle.DRIZZLE_DEFAULT_SOCKET_RECV_SIZE
DRIZZLE_RETURN_OK = _libdrizzle.DRIZZLE_RETURN_OK
DRIZZLE_RETURN_IO_WAIT = _libdrizzle.DRIZZLE_RETURN_IO_WAIT
DRIZZLE_RETURN_PAUSE = _libdrizzle.DRIZZLE_RETURN_PAUSE
DRIZZLE_RETURN_ROW_BREAK = _libdrizzle.DRIZZLE_RETURN_ROW_BREAK
DRIZZLE_RETURN_MEMORY = _libdrizzle.DRIZZLE_RETURN_MEMORY
DRIZZLE_RETURN_ERRNO = _libdrizzle.DRIZZLE_RETURN_ERRNO
DRIZZLE_RETURN_INTERNAL_ERROR = _libdrizzle.DRIZZLE_RETURN_INTERNAL_ERROR
DRIZZLE_RETURN_GETADDRINFO = _libdrizzle.DRIZZLE_RETURN_GETADDRINFO
DRIZZLE_RETURN_NOT_READY = _libdrizzle.DRIZZLE_RETURN_NOT_READY
DRIZZLE_RETURN_BAD_PACKET_NUMBER = _libdrizzle.DRIZZLE_RETURN_BAD_PACKET_NUMBER
DRIZZLE_RETURN_BAD_HANDSHAKE_PACKET = _libdrizzle.DRIZZLE_RETURN_BAD_HANDSHAKE_PACKET
DRIZZLE_RETURN_BAD_PACKET = _libdrizzle.DRIZZLE_RETURN_BAD_PACKET
DRIZZLE_RETURN_PROTOCOL_NOT_SUPPORTED = _libdrizzle.DRIZZLE_RETURN_PROTOCOL_NOT_SUPPORTED
DRIZZLE_RETURN_UNEXPECTED_DATA = _libdrizzle.DRIZZLE_RETURN_UNEXPECTED_DATA
DRIZZLE_RETURN_NO_SCRAMBLE = _libdrizzle.DRIZZLE_RETURN_NO_SCRAMBLE
DRIZZLE_RETURN_AUTH_FAILED = _libdrizzle.DRIZZLE_RETURN_AUTH_FAILED
DRIZZLE_RETURN_NULL_SIZE = _libdrizzle.DRIZZLE_RETURN_NULL_SIZE
DRIZZLE_RETURN_ERROR_CODE = _libdrizzle.DRIZZLE_RETURN_ERROR_CODE
DRIZZLE_RETURN_TOO_MANY_COLUMNS = _libdrizzle.DRIZZLE_RETURN_TOO_MANY_COLUMNS
DRIZZLE_RETURN_ROW_END = _libdrizzle.DRIZZLE_RETURN_ROW_END
DRIZZLE_RETURN_LOST_CONNECTION = _libdrizzle.DRIZZLE_RETURN_LOST_CONNECTION
DRIZZLE_RETURN_COULD_NOT_CONNECT = _libdrizzle.DRIZZLE_RETURN_COULD_NOT_CONNECT
DRIZZLE_RETURN_NO_ACTIVE_CONNECTIONS = _libdrizzle.DRIZZLE_RETURN_NO_ACTIVE_CONNECTIONS
DRIZZLE_RETURN_HANDSHAKE_FAILED = _libdrizzle.DRIZZLE_RETURN_HANDSHAKE_FAILED
DRIZZLE_RETURN_MAX = _libdrizzle.DRIZZLE_RETURN_MAX
DRIZZLE_COLUMN_TYPE_VIRTUAL = _libdrizzle.DRIZZLE_COLUMN_TYPE_VIRTUAL
DRIZZLE_NONE = _libdrizzle.DRIZZLE_NONE
DRIZZLE_ALLOCATED = _libdrizzle.DRIZZLE_ALLOCATED
DRIZZLE_NON_BLOCKING = _libdrizzle.DRIZZLE_NON_BLOCKING
DRIZZLE_AUTO_ALLOCATED = _libdrizzle.DRIZZLE_AUTO_ALLOCATED
DRIZZLE_CON_NONE = _libdrizzle.DRIZZLE_CON_NONE
DRIZZLE_CON_ALLOCATED = _libdrizzle.DRIZZLE_CON_ALLOCATED
DRIZZLE_CON_MYSQL = _libdrizzle.DRIZZLE_CON_MYSQL
DRIZZLE_CON_RAW_PACKET = _libdrizzle.DRIZZLE_CON_RAW_PACKET
DRIZZLE_CON_RAW_SCRAMBLE = _libdrizzle.DRIZZLE_CON_RAW_SCRAMBLE
DRIZZLE_CON_READY = _libdrizzle.DRIZZLE_CON_READY
DRIZZLE_CON_NO_RESULT_READ = _libdrizzle.DRIZZLE_CON_NO_RESULT_READ
DRIZZLE_CON_IO_READY = _libdrizzle.DRIZZLE_CON_IO_READY
DRIZZLE_CON_STATUS_NONE = _libdrizzle.DRIZZLE_CON_STATUS_NONE
DRIZZLE_CON_STATUS_IN_TRANS = _libdrizzle.DRIZZLE_CON_STATUS_IN_TRANS
DRIZZLE_CON_STATUS_AUTOCOMMIT = _libdrizzle.DRIZZLE_CON_STATUS_AUTOCOMMIT
DRIZZLE_CON_STATUS_MORE_RESULTS_EXISTS = _libdrizzle.DRIZZLE_CON_STATUS_MORE_RESULTS_EXISTS
DRIZZLE_CON_STATUS_QUERY_NO_GOOD_INDEX_USED = _libdrizzle.DRIZZLE_CON_STATUS_QUERY_NO_GOOD_INDEX_USED
DRIZZLE_CON_STATUS_QUERY_NO_INDEX_USED = _libdrizzle.DRIZZLE_CON_STATUS_QUERY_NO_INDEX_USED
DRIZZLE_CON_STATUS_CURSOR_EXISTS = _libdrizzle.DRIZZLE_CON_STATUS_CURSOR_EXISTS
DRIZZLE_CON_STATUS_LAST_ROW_SENT = _libdrizzle.DRIZZLE_CON_STATUS_LAST_ROW_SENT
DRIZZLE_CON_STATUS_DB_DROPPED = _libdrizzle.DRIZZLE_CON_STATUS_DB_DROPPED
DRIZZLE_CON_STATUS_NO_BACKSLASH_ESCAPES = _libdrizzle.DRIZZLE_CON_STATUS_NO_BACKSLASH_ESCAPES
DRIZZLE_CON_STATUS_QUERY_WAS_SLOW = _libdrizzle.DRIZZLE_CON_STATUS_QUERY_WAS_SLOW
DRIZZLE_CAPABILITIES_NONE = _libdrizzle.DRIZZLE_CAPABILITIES_NONE
DRIZZLE_CAPABILITIES_LONG_PASSWORD = _libdrizzle.DRIZZLE_CAPABILITIES_LONG_PASSWORD
DRIZZLE_CAPABILITIES_FOUND_ROWS = _libdrizzle.DRIZZLE_CAPABILITIES_FOUND_ROWS
DRIZZLE_CAPABILITIES_LONG_FLAG = _libdrizzle.DRIZZLE_CAPABILITIES_LONG_FLAG
DRIZZLE_CAPABILITIES_CONNECT_WITH_DB = _libdrizzle.DRIZZLE_CAPABILITIES_CONNECT_WITH_DB
DRIZZLE_CAPABILITIES_NO_SCHEMA = _libdrizzle.DRIZZLE_CAPABILITIES_NO_SCHEMA
DRIZZLE_CAPABILITIES_COMPRESS = _libdrizzle.DRIZZLE_CAPABILITIES_COMPRESS
DRIZZLE_CAPABILITIES_ODBC = _libdrizzle.DRIZZLE_CAPABILITIES_ODBC
DRIZZLE_CAPABILITIES_LOCAL_FILES = _libdrizzle.DRIZZLE_CAPABILITIES_LOCAL_FILES
DRIZZLE_CAPABILITIES_IGNORE_SPACE = _libdrizzle.DRIZZLE_CAPABILITIES_IGNORE_SPACE
DRIZZLE_CAPABILITIES_PROTOCOL_41 = _libdrizzle.DRIZZLE_CAPABILITIES_PROTOCOL_41
DRIZZLE_CAPABILITIES_INTERACTIVE = _libdrizzle.DRIZZLE_CAPABILITIES_INTERACTIVE
DRIZZLE_CAPABILITIES_SSL = _libdrizzle.DRIZZLE_CAPABILITIES_SSL
DRIZZLE_CAPABILITIES_IGNORE_SIGPIPE = _libdrizzle.DRIZZLE_CAPABILITIES_IGNORE_SIGPIPE
DRIZZLE_CAPABILITIES_TRANSACTIONS = _libdrizzle.DRIZZLE_CAPABILITIES_TRANSACTIONS
DRIZZLE_CAPABILITIES_RESERVED = _libdrizzle.DRIZZLE_CAPABILITIES_RESERVED
DRIZZLE_CAPABILITIES_SECURE_CONNECTION = _libdrizzle.DRIZZLE_CAPABILITIES_SECURE_CONNECTION
DRIZZLE_CAPABILITIES_MULTI_STATEMENTS = _libdrizzle.DRIZZLE_CAPABILITIES_MULTI_STATEMENTS
DRIZZLE_CAPABILITIES_MULTI_RESULTS = _libdrizzle.DRIZZLE_CAPABILITIES_MULTI_RESULTS
DRIZZLE_CAPABILITIES_SSL_VERIFY_SERVER_CERT = _libdrizzle.DRIZZLE_CAPABILITIES_SSL_VERIFY_SERVER_CERT
DRIZZLE_CAPABILITIES_REMEMBER_OPTIONS = _libdrizzle.DRIZZLE_CAPABILITIES_REMEMBER_OPTIONS
DRIZZLE_CAPABILITIES_CLIENT = _libdrizzle.DRIZZLE_CAPABILITIES_CLIENT
DRIZZLE_COMMAND_SLEEP = _libdrizzle.DRIZZLE_COMMAND_SLEEP
DRIZZLE_COMMAND_QUIT = _libdrizzle.DRIZZLE_COMMAND_QUIT
DRIZZLE_COMMAND_INIT_DB = _libdrizzle.DRIZZLE_COMMAND_INIT_DB
DRIZZLE_COMMAND_QUERY = _libdrizzle.DRIZZLE_COMMAND_QUERY
DRIZZLE_COMMAND_FIELD_LIST = _libdrizzle.DRIZZLE_COMMAND_FIELD_LIST
DRIZZLE_COMMAND_CREATE_DB = _libdrizzle.DRIZZLE_COMMAND_CREATE_DB
DRIZZLE_COMMAND_DROP_DB = _libdrizzle.DRIZZLE_COMMAND_DROP_DB
DRIZZLE_COMMAND_REFRESH = _libdrizzle.DRIZZLE_COMMAND_REFRESH
DRIZZLE_COMMAND_SHUTDOWN = _libdrizzle.DRIZZLE_COMMAND_SHUTDOWN
DRIZZLE_COMMAND_STATISTICS = _libdrizzle.DRIZZLE_COMMAND_STATISTICS
DRIZZLE_COMMAND_PROCESS_INFO = _libdrizzle.DRIZZLE_COMMAND_PROCESS_INFO
DRIZZLE_COMMAND_CONNECT = _libdrizzle.DRIZZLE_COMMAND_CONNECT
DRIZZLE_COMMAND_PROCESS_KILL = _libdrizzle.DRIZZLE_COMMAND_PROCESS_KILL
DRIZZLE_COMMAND_DEBUG = _libdrizzle.DRIZZLE_COMMAND_DEBUG
DRIZZLE_COMMAND_PING = _libdrizzle.DRIZZLE_COMMAND_PING
DRIZZLE_COMMAND_TIME = _libdrizzle.DRIZZLE_COMMAND_TIME
DRIZZLE_COMMAND_DELAYED_INSERT = _libdrizzle.DRIZZLE_COMMAND_DELAYED_INSERT
DRIZZLE_COMMAND_CHANGE_USER = _libdrizzle.DRIZZLE_COMMAND_CHANGE_USER
DRIZZLE_COMMAND_BINLOG_DUMP = _libdrizzle.DRIZZLE_COMMAND_BINLOG_DUMP
DRIZZLE_COMMAND_TABLE_DUMP = _libdrizzle.DRIZZLE_COMMAND_TABLE_DUMP
DRIZZLE_COMMAND_CONNECT_OUT = _libdrizzle.DRIZZLE_COMMAND_CONNECT_OUT
DRIZZLE_COMMAND_REGISTER_SLAVE = _libdrizzle.DRIZZLE_COMMAND_REGISTER_SLAVE
DRIZZLE_COMMAND_STMT_PREPARE = _libdrizzle.DRIZZLE_COMMAND_STMT_PREPARE
DRIZZLE_COMMAND_STMT_EXECUTE = _libdrizzle.DRIZZLE_COMMAND_STMT_EXECUTE
DRIZZLE_COMMAND_STMT_SEND_LONG_DATA = _libdrizzle.DRIZZLE_COMMAND_STMT_SEND_LONG_DATA
DRIZZLE_COMMAND_STMT_CLOSE = _libdrizzle.DRIZZLE_COMMAND_STMT_CLOSE
DRIZZLE_COMMAND_STMT_RESET = _libdrizzle.DRIZZLE_COMMAND_STMT_RESET
DRIZZLE_COMMAND_SET_OPTION = _libdrizzle.DRIZZLE_COMMAND_SET_OPTION
DRIZZLE_COMMAND_STMT_FETCH = _libdrizzle.DRIZZLE_COMMAND_STMT_FETCH
DRIZZLE_COMMAND_DAEMON = _libdrizzle.DRIZZLE_COMMAND_DAEMON
DRIZZLE_COMMAND_END = _libdrizzle.DRIZZLE_COMMAND_END
DRIZZLE_COMMAND_DRIZZLE_SLEEP = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_SLEEP
DRIZZLE_COMMAND_DRIZZLE_QUIT = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_QUIT
DRIZZLE_COMMAND_DRIZZLE_INIT_DB = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_INIT_DB
DRIZZLE_COMMAND_DRIZZLE_QUERY = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_QUERY
DRIZZLE_COMMAND_DRIZZLE_SHUTDOWN = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_SHUTDOWN
DRIZZLE_COMMAND_DRIZZLE_CONNECT = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_CONNECT
DRIZZLE_COMMAND_DRIZZLE_PING = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_PING
DRIZZLE_COMMAND_DRIZZLE_END = _libdrizzle.DRIZZLE_COMMAND_DRIZZLE_END
DRIZZLE_REFRESH_GRANT = _libdrizzle.DRIZZLE_REFRESH_GRANT
DRIZZLE_REFRESH_LOG = _libdrizzle.DRIZZLE_REFRESH_LOG
DRIZZLE_REFRESH_TABLES = _libdrizzle.DRIZZLE_REFRESH_TABLES
DRIZZLE_REFRESH_HOSTS = _libdrizzle.DRIZZLE_REFRESH_HOSTS
DRIZZLE_REFRESH_STATUS = _libdrizzle.DRIZZLE_REFRESH_STATUS
DRIZZLE_REFRESH_THREADS = _libdrizzle.DRIZZLE_REFRESH_THREADS
DRIZZLE_REFRESH_SLAVE = _libdrizzle.DRIZZLE_REFRESH_SLAVE
DRIZZLE_REFRESH_MASTER = _libdrizzle.DRIZZLE_REFRESH_MASTER
DRIZZLE_SHUTDOWN_DEFAULT = _libdrizzle.DRIZZLE_SHUTDOWN_DEFAULT
DRIZZLE_SHUTDOWN_WAIT_CONNECTIONS = _libdrizzle.DRIZZLE_SHUTDOWN_WAIT_CONNECTIONS
DRIZZLE_SHUTDOWN_WAIT_TRANSACTIONS = _libdrizzle.DRIZZLE_SHUTDOWN_WAIT_TRANSACTIONS
DRIZZLE_SHUTDOWN_WAIT_UPDATES = _libdrizzle.DRIZZLE_SHUTDOWN_WAIT_UPDATES
DRIZZLE_SHUTDOWN_WAIT_ALL_BUFFERS = _libdrizzle.DRIZZLE_SHUTDOWN_WAIT_ALL_BUFFERS
DRIZZLE_SHUTDOWN_WAIT_CRITICAL_BUFFERS = _libdrizzle.DRIZZLE_SHUTDOWN_WAIT_CRITICAL_BUFFERS
DRIZZLE_SHUTDOWN_KILL_QUERY = _libdrizzle.DRIZZLE_SHUTDOWN_KILL_QUERY
DRIZZLE_SHUTDOWN_KILL_CONNECTION = _libdrizzle.DRIZZLE_SHUTDOWN_KILL_CONNECTION
DRIZZLE_QUERY_ALLOCATED = _libdrizzle.DRIZZLE_QUERY_ALLOCATED
DRIZZLE_QUERY_STATE_INIT = _libdrizzle.DRIZZLE_QUERY_STATE_INIT
DRIZZLE_QUERY_STATE_QUERY = _libdrizzle.DRIZZLE_QUERY_STATE_QUERY
DRIZZLE_QUERY_STATE_RESULT = _libdrizzle.DRIZZLE_QUERY_STATE_RESULT
DRIZZLE_QUERY_STATE_DONE = _libdrizzle.DRIZZLE_QUERY_STATE_DONE
DRIZZLE_RESULT_NONE = _libdrizzle.DRIZZLE_RESULT_NONE
DRIZZLE_RESULT_ALLOCATED = _libdrizzle.DRIZZLE_RESULT_ALLOCATED
DRIZZLE_RESULT_SKIP_COLUMN = _libdrizzle.DRIZZLE_RESULT_SKIP_COLUMN
DRIZZLE_RESULT_BUFFER_COLUMN = _libdrizzle.DRIZZLE_RESULT_BUFFER_COLUMN
DRIZZLE_RESULT_BUFFER_ROW = _libdrizzle.DRIZZLE_RESULT_BUFFER_ROW
DRIZZLE_RESULT_EOF_PACKET = _libdrizzle.DRIZZLE_RESULT_EOF_PACKET
DRIZZLE_RESULT_ROW_BREAK = _libdrizzle.DRIZZLE_RESULT_ROW_BREAK
DRIZZLE_COLUMN_ALLOCATED = _libdrizzle.DRIZZLE_COLUMN_ALLOCATED
DRIZZLE_COLUMN_TYPE_DECIMAL = _libdrizzle.DRIZZLE_COLUMN_TYPE_DECIMAL
DRIZZLE_COLUMN_TYPE_TINY = _libdrizzle.DRIZZLE_COLUMN_TYPE_TINY
DRIZZLE_COLUMN_TYPE_SHORT = _libdrizzle.DRIZZLE_COLUMN_TYPE_SHORT
DRIZZLE_COLUMN_TYPE_LONG = _libdrizzle.DRIZZLE_COLUMN_TYPE_LONG
DRIZZLE_COLUMN_TYPE_FLOAT = _libdrizzle.DRIZZLE_COLUMN_TYPE_FLOAT
DRIZZLE_COLUMN_TYPE_DOUBLE = _libdrizzle.DRIZZLE_COLUMN_TYPE_DOUBLE
DRIZZLE_COLUMN_TYPE_NULL = _libdrizzle.DRIZZLE_COLUMN_TYPE_NULL
DRIZZLE_COLUMN_TYPE_TIMESTAMP = _libdrizzle.DRIZZLE_COLUMN_TYPE_TIMESTAMP
DRIZZLE_COLUMN_TYPE_LONGLONG = _libdrizzle.DRIZZLE_COLUMN_TYPE_LONGLONG
DRIZZLE_COLUMN_TYPE_INT24 = _libdrizzle.DRIZZLE_COLUMN_TYPE_INT24
DRIZZLE_COLUMN_TYPE_DATE = _libdrizzle.DRIZZLE_COLUMN_TYPE_DATE
DRIZZLE_COLUMN_TYPE_TIME = _libdrizzle.DRIZZLE_COLUMN_TYPE_TIME
DRIZZLE_COLUMN_TYPE_DATETIME = _libdrizzle.DRIZZLE_COLUMN_TYPE_DATETIME
DRIZZLE_COLUMN_TYPE_YEAR = _libdrizzle.DRIZZLE_COLUMN_TYPE_YEAR
DRIZZLE_COLUMN_TYPE_NEWDATE = _libdrizzle.DRIZZLE_COLUMN_TYPE_NEWDATE
DRIZZLE_COLUMN_TYPE_VARCHAR = _libdrizzle.DRIZZLE_COLUMN_TYPE_VARCHAR
DRIZZLE_COLUMN_TYPE_BIT = _libdrizzle.DRIZZLE_COLUMN_TYPE_BIT
DRIZZLE_COLUMN_TYPE_NEWDECIMAL = _libdrizzle.DRIZZLE_COLUMN_TYPE_NEWDECIMAL
DRIZZLE_COLUMN_TYPE_ENUM = _libdrizzle.DRIZZLE_COLUMN_TYPE_ENUM
DRIZZLE_COLUMN_TYPE_SET = _libdrizzle.DRIZZLE_COLUMN_TYPE_SET
DRIZZLE_COLUMN_TYPE_TINY_BLOB = _libdrizzle.DRIZZLE_COLUMN_TYPE_TINY_BLOB
DRIZZLE_COLUMN_TYPE_MEDIUM_BLOB = _libdrizzle.DRIZZLE_COLUMN_TYPE_MEDIUM_BLOB
DRIZZLE_COLUMN_TYPE_LONG_BLOB = _libdrizzle.DRIZZLE_COLUMN_TYPE_LONG_BLOB
DRIZZLE_COLUMN_TYPE_BLOB = _libdrizzle.DRIZZLE_COLUMN_TYPE_BLOB
DRIZZLE_COLUMN_TYPE_VAR_STRING = _libdrizzle.DRIZZLE_COLUMN_TYPE_VAR_STRING
DRIZZLE_COLUMN_TYPE_STRING = _libdrizzle.DRIZZLE_COLUMN_TYPE_STRING
DRIZZLE_COLUMN_TYPE_GEOMETRY = _libdrizzle.DRIZZLE_COLUMN_TYPE_GEOMETRY
DRIZZLE_COLUMN_TYPE_DRIZZLE_TINY = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_TINY
DRIZZLE_COLUMN_TYPE_DRIZZLE_LONG = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_LONG
DRIZZLE_COLUMN_TYPE_DRIZZLE_DOUBLE = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_DOUBLE
DRIZZLE_COLUMN_TYPE_DRIZZLE_NULL = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_NULL
DRIZZLE_COLUMN_TYPE_DRIZZLE_TIMESTAMP = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_TIMESTAMP
DRIZZLE_COLUMN_TYPE_DRIZZLE_LONGLONG = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_LONGLONG
DRIZZLE_COLUMN_TYPE_DRIZZLE_DATETIME = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_DATETIME
DRIZZLE_COLUMN_TYPE_DRIZZLE_DATE = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_DATE
DRIZZLE_COLUMN_TYPE_DRIZZLE_VARCHAR = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_VARCHAR
DRIZZLE_COLUMN_TYPE_DRIZZLE_NEWDECIMAL = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_NEWDECIMAL
DRIZZLE_COLUMN_TYPE_DRIZZLE_ENUM = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_ENUM
DRIZZLE_COLUMN_TYPE_DRIZZLE_BLOB = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_BLOB
DRIZZLE_COLUMN_TYPE_DRIZZLE_MAX = _libdrizzle.DRIZZLE_COLUMN_TYPE_DRIZZLE_MAX
DRIZZLE_COLUMN_FLAGS_NONE = _libdrizzle.DRIZZLE_COLUMN_FLAGS_NONE
DRIZZLE_COLUMN_FLAGS_NOT_NULL = _libdrizzle.DRIZZLE_COLUMN_FLAGS_NOT_NULL
DRIZZLE_COLUMN_FLAGS_PRI_KEY = _libdrizzle.DRIZZLE_COLUMN_FLAGS_PRI_KEY
DRIZZLE_COLUMN_FLAGS_UNIQUE_KEY = _libdrizzle.DRIZZLE_COLUMN_FLAGS_UNIQUE_KEY
DRIZZLE_COLUMN_FLAGS_MULTIPLE_KEY = _libdrizzle.DRIZZLE_COLUMN_FLAGS_MULTIPLE_KEY
DRIZZLE_COLUMN_FLAGS_BLOB = _libdrizzle.DRIZZLE_COLUMN_FLAGS_BLOB
DRIZZLE_COLUMN_FLAGS_UNSIGNED = _libdrizzle.DRIZZLE_COLUMN_FLAGS_UNSIGNED
DRIZZLE_COLUMN_FLAGS_ZEROFILL = _libdrizzle.DRIZZLE_COLUMN_FLAGS_ZEROFILL
DRIZZLE_COLUMN_FLAGS_BINARY = _libdrizzle.DRIZZLE_COLUMN_FLAGS_BINARY
DRIZZLE_COLUMN_FLAGS_ENUM = _libdrizzle.DRIZZLE_COLUMN_FLAGS_ENUM
DRIZZLE_COLUMN_FLAGS_AUTO_INCREMENT = _libdrizzle.DRIZZLE_COLUMN_FLAGS_AUTO_INCREMENT
DRIZZLE_COLUMN_FLAGS_TIMESTAMP = _libdrizzle.DRIZZLE_COLUMN_FLAGS_TIMESTAMP
DRIZZLE_COLUMN_FLAGS_SET = _libdrizzle.DRIZZLE_COLUMN_FLAGS_SET
DRIZZLE_COLUMN_FLAGS_NO_DEFAULT_VALUE = _libdrizzle.DRIZZLE_COLUMN_FLAGS_NO_DEFAULT_VALUE
DRIZZLE_COLUMN_FLAGS_ON_UPDATE_NOW = _libdrizzle.DRIZZLE_COLUMN_FLAGS_ON_UPDATE_NOW
DRIZZLE_COLUMN_FLAGS_PART_KEY = _libdrizzle.DRIZZLE_COLUMN_FLAGS_PART_KEY
DRIZZLE_COLUMN_FLAGS_NUM = _libdrizzle.DRIZZLE_COLUMN_FLAGS_NUM
DRIZZLE_COLUMN_FLAGS_GROUP = _libdrizzle.DRIZZLE_COLUMN_FLAGS_GROUP
DRIZZLE_COLUMN_FLAGS_UNIQUE = _libdrizzle.DRIZZLE_COLUMN_FLAGS_UNIQUE
DRIZZLE_COLUMN_FLAGS_BINCMP = _libdrizzle.DRIZZLE_COLUMN_FLAGS_BINCMP
DRIZZLE_COLUMN_FLAGS_GET_FIXED_FIELDS = _libdrizzle.DRIZZLE_COLUMN_FLAGS_GET_FIXED_FIELDS
DRIZZLE_COLUMN_FLAGS_IN_PART_FUNC = _libdrizzle.DRIZZLE_COLUMN_FLAGS_IN_PART_FUNC
DRIZZLE_COLUMN_FLAGS_IN_ADD_INDEX = _libdrizzle.DRIZZLE_COLUMN_FLAGS_IN_ADD_INDEX
DRIZZLE_COLUMN_FLAGS_RENAMED = _libdrizzle.DRIZZLE_COLUMN_FLAGS_RENAMED
DrizzleException = _libdrizzle.DrizzleException
Warning = _libdrizzle.Warning
Error = _libdrizzle.Error
InterfaceError = _libdrizzle.InterfaceError
DatabaseError = _libdrizzle.DatabaseError
DataError = _libdrizzle.DataError
OperationalError = _libdrizzle.OperationalError
IntegrityError = _libdrizzle.IntegrityError
InternalError = _libdrizzle.InternalError
ProgrammingError = _libdrizzle.ProgrammingError
NotSupportedError = _libdrizzle.NotSupportedError

def drizzle_version() -> 'char *':
    return _libdrizzle.drizzle_version()


drizzle_version = _libdrizzle.drizzle_version

class Drizzle(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Drizzle, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Drizzle, name)
    __repr__ = _swig_repr

    def __init__(self):
        this = _libdrizzle.new_Drizzle()
        try:
            self.this.append(this)
        except:
            self.this = this

    __swig_destroy__ = _libdrizzle.delete_Drizzle
    __del__ = lambda self: None

    def copy(self) -> 'drizzle *':
        return _libdrizzle.Drizzle_copy(self)

    def error(self) -> 'char const *':
        return _libdrizzle.Drizzle_error(self)

    def errno(self) -> 'int':
        return _libdrizzle.Drizzle_errno(self)

    def options(self) -> 'drizzle_options_t':
        return _libdrizzle.Drizzle_options(self)

    def set_options(self, *args) -> 'void':
        return _libdrizzle.Drizzle_set_options(self, *args)

    def add_options(self, *args) -> 'void':
        return _libdrizzle.Drizzle_add_options(self, *args)

    def remove_options(self, *args) -> 'void':
        return _libdrizzle.Drizzle_remove_options(self, *args)

    def create_client_connection(self) -> 'Client *':
        return _libdrizzle.Drizzle_create_client_connection(self)

    def create_server_connection(self) -> 'Server *':
        return _libdrizzle.Drizzle_create_server_connection(self)

    def con_wait(self) -> 'drizzle_return_t':
        return _libdrizzle.Drizzle_con_wait(self)

    def con_ready(self) -> 'drizzle_con *':
        return _libdrizzle.Drizzle_con_ready(self)

    def add_tcp(self, *args) -> 'Client *':
        return _libdrizzle.Drizzle_add_tcp(self, *args)

    def add_uds(self, *args) -> 'Client *':
        return _libdrizzle.Drizzle_add_uds(self, *args)

    def query_create(self, *args) -> 'drizzle_query_st *':
        return _libdrizzle.Drizzle_query_create(self, *args)

    def query_add(self, *args) -> 'drizzle_query_st *':
        return _libdrizzle.Drizzle_query_add(self, *args)

    def run(self) -> 'drizzle_query_st *':
        return _libdrizzle.Drizzle_run(self)

    def query_run_all(self) -> 'drizzle_return_t':
        return _libdrizzle.Drizzle_query_run_all(self)


Drizzle_swigregister = _libdrizzle.Drizzle_swigregister
Drizzle_swigregister(Drizzle)

class Connection(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Connection, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Connection, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr
    __swig_destroy__ = _libdrizzle.delete_Connection
    __del__ = lambda self: None

    def copy(self) -> 'drizzle_con *':
        return _libdrizzle.Connection_copy(self)

    def host(self) -> 'char const *':
        return _libdrizzle.Connection_host(self)

    def port(self) -> 'in_port_t':
        return _libdrizzle.Connection_port(self)

    def set_tcp(self, *args) -> 'void':
        return _libdrizzle.Connection_set_tcp(self, *args)

    def uds(self) -> 'char const *':
        return _libdrizzle.Connection_uds(self)

    def set_uds(self, *args) -> 'void':
        return _libdrizzle.Connection_set_uds(self, *args)

    def user(self) -> 'char const *':
        return _libdrizzle.Connection_user(self)

    def password(self) -> 'char const *':
        return _libdrizzle.Connection_password(self)

    def set_auth(self, *args) -> 'void':
        return _libdrizzle.Connection_set_auth(self, *args)

    def db(self) -> 'char const *':
        return _libdrizzle.Connection_db(self)

    def set_db(self, *args) -> 'void':
        return _libdrizzle.Connection_set_db(self, *args)

    def options(self) -> 'drizzle_con_options_t':
        return _libdrizzle.Connection_options(self)

    def set_options(self, *args) -> 'void':
        return _libdrizzle.Connection_set_options(self, *args)

    def add_options(self, *args) -> 'void':
        return _libdrizzle.Connection_add_options(self, *args)

    def remove_options(self, *args) -> 'void':
        return _libdrizzle.Connection_remove_options(self, *args)

    def connect(self) -> 'drizzle_return_t':
        return _libdrizzle.Connection_connect(self)

    def close(self) -> 'void':
        return _libdrizzle.Connection_close(self)

    def protocol_version(self) -> 'uint8_t':
        return _libdrizzle.Connection_protocol_version(self)

    def server_version(self) -> 'char const *':
        return _libdrizzle.Connection_server_version(self)

    def server_version_number(self) -> 'uint32_t':
        return _libdrizzle.Connection_server_version_number(self)

    def thread_id(self) -> 'uint32_t':
        return _libdrizzle.Connection_thread_id(self)

    def scramble(self) -> 'uint8_t const *':
        return _libdrizzle.Connection_scramble(self)

    def capabilities(self) -> 'drizzle_capabilities_t':
        return _libdrizzle.Connection_capabilities(self)

    def charset(self) -> 'drizzle_charset_t':
        return _libdrizzle.Connection_charset(self)

    def status(self) -> 'drizzle_con_status_t':
        return _libdrizzle.Connection_status(self)

    def max_packet_size(self) -> 'uint32_t':
        return _libdrizzle.Connection_max_packet_size(self)


Connection_swigregister = _libdrizzle.Connection_swigregister
Connection_swigregister(Connection)

class Client(Connection):
    __swig_setmethods__ = {}
    for _s in [Connection]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))

    __setattr__ = lambda self, name, value: _swig_setattr(self, Client, name, value)
    __swig_getmethods__ = {}
    for _s in [Connection]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))

    __getattr__ = lambda self, name: _swig_getattr(self, Client, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr

    def buffer_query(self, *args) -> 'result_client_buffered *':
        return _libdrizzle.Client_buffer_query(self, *args)

    def query(self, *args) -> 'result_client_unbuffered *':
        return _libdrizzle.Client_query(self, *args)

    def query_inc(self, *args) -> 'result_client_unbuffered *':
        return _libdrizzle.Client_query_inc(self, *args)

    def quit(self) -> 'result_client *':
        return _libdrizzle.Client_quit(self)

    def select_db(self, *args) -> 'result_client *':
        return _libdrizzle.Client_select_db(self, *args)

    def refresh(self, *args) -> 'result_client *':
        return _libdrizzle.Client_refresh(self, *args)

    def shutdown(self, *args) -> 'result_client *':
        return _libdrizzle.Client_shutdown(self, *args)

    def stat(self) -> 'result_client *':
        return _libdrizzle.Client_stat(self)

    def debug_info(self) -> 'result_client *':
        return _libdrizzle.Client_debug_info(self)

    def ping(self) -> 'result_client *':
        return _libdrizzle.Client_ping(self)

    def change_user(self, *args) -> 'result_client *':
        return _libdrizzle.Client_change_user(self, *args)

    def write(self, *args) -> 'result_server *':
        return _libdrizzle.Client_write(self, *args)

    def result_read(self, to: 'drizzle_result_st'=None) -> 'result_client *':
        return _libdrizzle.Client_result_read(self, to)

    def result_create(self, to: 'drizzle_result_st'=None) -> 'result_client *':
        return _libdrizzle.Client_result_create(self, to)

    def result_clone(self, *args) -> 'result_client *':
        return _libdrizzle.Client_result_clone(self, *args)

    __swig_destroy__ = _libdrizzle.delete_Client
    __del__ = lambda self: None


Client_swigregister = _libdrizzle.Client_swigregister
Client_swigregister(Client)

class Server(Connection):
    __swig_setmethods__ = {}
    for _s in [Connection]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))

    __setattr__ = lambda self, name, value: _swig_setattr(self, Server, name, value)
    __swig_getmethods__ = {}
    for _s in [Connection]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))

    __getattr__ = lambda self, name: _swig_getattr(self, Server, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr

    def set_protocol_version(self, *args) -> 'void':
        return _libdrizzle.Server_set_protocol_version(self, *args)

    def set_server_version(self, *args) -> 'void':
        return _libdrizzle.Server_set_server_version(self, *args)

    def set_thread_id(self, *args) -> 'void':
        return _libdrizzle.Server_set_thread_id(self, *args)

    def set_scramble(self, *args) -> 'void':
        return _libdrizzle.Server_set_scramble(self, *args)

    def set_capabilities(self, *args) -> 'void':
        return _libdrizzle.Server_set_capabilities(self, *args)

    def set_charset(self, *args) -> 'void':
        return _libdrizzle.Server_set_charset(self, *args)

    def set_status(self, *args) -> 'void':
        return _libdrizzle.Server_set_status(self, *args)

    def set_max_packet_size(self, *args) -> 'void':
        return _libdrizzle.Server_set_max_packet_size(self, *args)

    def copy_handshake(self, *args) -> 'void':
        return _libdrizzle.Server_copy_handshake(self, *args)

    def result_create(self, to: 'drizzle_result_st'=None) -> 'result_server *':
        return _libdrizzle.Server_result_create(self, to)

    def result_clone(self, *args) -> 'result_server *':
        return _libdrizzle.Server_result_clone(self, *args)

    def result_write(self, *args) -> 'drizzle_return_t':
        return _libdrizzle.Server_result_write(self, *args)

    __swig_destroy__ = _libdrizzle.delete_Server
    __del__ = lambda self: None


Server_swigregister = _libdrizzle.Server_swigregister
Server_swigregister(Server)

class Query(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Query, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Query, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr
    __swig_destroy__ = _libdrizzle.delete_Query
    __del__ = lambda self: None

    def con(self) -> 'drizzle_con *':
        return _libdrizzle.Query_con(self)

    def set_con(self, *args) -> 'void':
        return _libdrizzle.Query_set_con(self, *args)

    def result_buffer(self) -> 'result_client_buffered *':
        return _libdrizzle.Query_result_buffer(self)

    def result(self) -> 'result_client_unbuffered *':
        return _libdrizzle.Query_result(self)

    def set_result(self, *args) -> 'void':
        return _libdrizzle.Query_set_result(self, *args)

    def string(self, *args) -> 'char *':
        return _libdrizzle.Query_string(self, *args)

    def set_string(self, *args) -> 'void':
        return _libdrizzle.Query_set_string(self, *args)

    def query_options(self) -> 'drizzle_query_options_t':
        return _libdrizzle.Query_query_options(self)

    def data(self) -> 'void *':
        return _libdrizzle.Query_data(self)

    def set_data(self, *args) -> 'void':
        return _libdrizzle.Query_set_data(self, *args)


Query_swigregister = _libdrizzle.Query_swigregister
Query_swigregister(Query)

class Result(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Result, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Result, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr
    __swig_destroy__ = _libdrizzle.delete_Result
    __del__ = lambda self: None

    def connection(self) -> 'drizzle_con *':
        return _libdrizzle.Result_connection(self)

    def eof(self) -> 'bool':
        return _libdrizzle.Result_eof(self)

    def info(self) -> 'char *':
        return _libdrizzle.Result_info(self)

    def error(self) -> 'char *':
        return _libdrizzle.Result_error(self)

    def error_code(self) -> 'uint16_t':
        return _libdrizzle.Result_error_code(self)

    def sqlstate(self) -> 'char *':
        return _libdrizzle.Result_sqlstate(self)

    def warning_count(self) -> 'uint16_t':
        return _libdrizzle.Result_warning_count(self)

    def insert_id(self) -> 'uint64_t':
        return _libdrizzle.Result_insert_id(self)

    def affected_rows(self) -> 'uint64_t':
        return _libdrizzle.Result_affected_rows(self)

    def column_count(self) -> 'uint16_t':
        return _libdrizzle.Result_column_count(self)

    def row_count(self) -> 'uint64_t':
        return _libdrizzle.Result_row_count(self)

    def row_next(self) -> 'char **':
        return _libdrizzle.Result_row_next(self)


Result_swigregister = _libdrizzle.Result_swigregister
Result_swigregister(Result)

class ResultClient(Result):
    __swig_setmethods__ = {}
    for _s in [Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))

    __setattr__ = lambda self, name, value: _swig_setattr(self, ResultClient, name, value)
    __swig_getmethods__ = {}
    for _s in [Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))

    __getattr__ = lambda self, name: _swig_getattr(self, ResultClient, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr

    def column_skip(self) -> 'drizzle_return_t':
        return _libdrizzle.ResultClient_column_skip(self)

    def column_read(self, column: 'Column'=None) -> 'drizzle_column *':
        return _libdrizzle.ResultClient_column_read(self, column)

    def column_buffer(self) -> 'drizzle_return_t':
        return _libdrizzle.ResultClient_column_buffer(self)

    def column_next(self) -> 'drizzle_column *':
        return _libdrizzle.ResultClient_column_next(self)

    def column_prev(self) -> 'drizzle_column *':
        return _libdrizzle.ResultClient_column_prev(self)

    def column_seek(self, *args) -> 'void':
        return _libdrizzle.ResultClient_column_seek(self, *args)

    def column_index(self, *args) -> 'drizzle_column *':
        return _libdrizzle.ResultClient_column_index(self, *args)

    def column_current(self) -> 'uint16_t':
        return _libdrizzle.ResultClient_column_current(self)

    __swig_destroy__ = _libdrizzle.delete_ResultClient
    __del__ = lambda self: None


ResultClient_swigregister = _libdrizzle.ResultClient_swigregister
ResultClient_swigregister(ResultClient)

class ResultClientBuffered(ResultClient):
    __swig_setmethods__ = {}
    for _s in [ResultClient]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))

    __setattr__ = lambda self, name, value: _swig_setattr(self, ResultClientBuffered, name, value)
    __swig_getmethods__ = {}
    for _s in [ResultClient]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))

    __getattr__ = lambda self, name: _swig_getattr(self, ResultClientBuffered, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr

    def row_field_sizes(self) -> 'size_t *':
        return _libdrizzle.ResultClientBuffered_row_field_sizes(self)

    def row_next(self) -> 'drizzle_row_t':
        return _libdrizzle.ResultClientBuffered_row_next(self)

    def row_prev(self) -> 'drizzle_row_t':
        return _libdrizzle.ResultClientBuffered_row_prev(self)

    def get_row_field(self, *args) -> 'char *':
        return _libdrizzle.ResultClientBuffered_get_row_field(self, *args)

    def row_seek(self, *args) -> 'void':
        return _libdrizzle.ResultClientBuffered_row_seek(self, *args)

    def row_index(self, *args) -> 'void':
        return _libdrizzle.ResultClientBuffered_row_index(self, *args)

    def row_current(self) -> 'uint64_t':
        return _libdrizzle.ResultClientBuffered_row_current(self)

    __swig_destroy__ = _libdrizzle.delete_ResultClientBuffered
    __del__ = lambda self: None


ResultClientBuffered_swigregister = _libdrizzle.ResultClientBuffered_swigregister
ResultClientBuffered_swigregister(ResultClientBuffered)

class ResultClientUnbuffered(ResultClient):
    __swig_setmethods__ = {}
    for _s in [ResultClient]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))

    __setattr__ = lambda self, name, value: _swig_setattr(self, ResultClientUnbuffered, name, value)
    __swig_getmethods__ = {}
    for _s in [ResultClient]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))

    __getattr__ = lambda self, name: _swig_getattr(self, ResultClientUnbuffered, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr

    def buffer_result(self) -> 'result_client_buffered *':
        return _libdrizzle.ResultClientUnbuffered_buffer_result(self)

    def field_buffer(self, *args) -> 'field':
        return _libdrizzle.ResultClientUnbuffered_field_buffer(self, *args)

    def field_read(self, *args) -> 'field':
        return _libdrizzle.ResultClientUnbuffered_field_read(self, *args)

    def row_read(self) -> 'uint64_t':
        return _libdrizzle.ResultClientUnbuffered_row_read(self)

    def row_buffer(self) -> 'void':
        return _libdrizzle.ResultClientUnbuffered_row_buffer(self)

    def row_free(self, *args) -> 'void':
        return _libdrizzle.ResultClientUnbuffered_row_free(self, *args)

    def row_current(self) -> 'uint64_t':
        return _libdrizzle.ResultClientUnbuffered_row_current(self)

    def field_free(self, *args) -> 'void':
        return _libdrizzle.ResultClientUnbuffered_field_free(self, *args)

    __swig_destroy__ = _libdrizzle.delete_ResultClientUnbuffered
    __del__ = lambda self: None


ResultClientUnbuffered_swigregister = _libdrizzle.ResultClientUnbuffered_swigregister
ResultClientUnbuffered_swigregister(ResultClientUnbuffered)

class ResultServer(Result):
    __swig_setmethods__ = {}
    for _s in [Result]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))

    __setattr__ = lambda self, name, value: _swig_setattr(self, ResultServer, name, value)
    __swig_getmethods__ = {}
    for _s in [Result]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))

    __getattr__ = lambda self, name: _swig_getattr(self, ResultServer, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr

    def set_eof(self, *args) -> 'void':
        return _libdrizzle.ResultServer_set_eof(self, *args)

    def set_info(self, *args) -> 'void':
        return _libdrizzle.ResultServer_set_info(self, *args)

    def set_error(self, *args) -> 'void':
        return _libdrizzle.ResultServer_set_error(self, *args)

    def set_error_code(self, *args) -> 'void':
        return _libdrizzle.ResultServer_set_error_code(self, *args)

    def set_sqlstate(self, *args) -> 'void':
        return _libdrizzle.ResultServer_set_sqlstate(self, *args)

    def set_warning_count(self, *args) -> 'void':
        return _libdrizzle.ResultServer_set_warning_count(self, *args)

    def set_insert_id(self, *args) -> 'void':
        return _libdrizzle.ResultServer_set_insert_id(self, *args)

    def set_affected_rows(self, *args) -> 'void':
        return _libdrizzle.ResultServer_set_affected_rows(self, *args)

    def set_column_count(self, *args) -> 'void':
        return _libdrizzle.ResultServer_set_column_count(self, *args)

    def column_create(self) -> 'column_server *':
        return _libdrizzle.ResultServer_column_create(self)

    def column_write(self, *args) -> 'drizzle_return_t':
        return _libdrizzle.ResultServer_column_write(self, *args)

    def row_write(self) -> 'drizzle_return_t':
        return _libdrizzle.ResultServer_row_write(self)

    __swig_destroy__ = _libdrizzle.delete_ResultServer
    __del__ = lambda self: None


ResultServer_swigregister = _libdrizzle.ResultServer_swigregister
ResultServer_swigregister(ResultServer)

class Column(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Column, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Column, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr
    __swig_destroy__ = _libdrizzle.delete_Column
    __del__ = lambda self: None

    def Result(self) -> 'drizzle_result *':
        return _libdrizzle.Column_Result(self)

    def catalog(self) -> 'char const *':
        return _libdrizzle.Column_catalog(self)

    def db(self) -> 'char const *':
        return _libdrizzle.Column_db(self)

    def table(self) -> 'char const *':
        return _libdrizzle.Column_table(self)

    def orig_table(self) -> 'char const *':
        return _libdrizzle.Column_orig_table(self)

    def name(self) -> 'char const *':
        return _libdrizzle.Column_name(self)

    def orig_name(self) -> 'char const *':
        return _libdrizzle.Column_orig_name(self)

    def charset(self) -> 'uint16_t const':
        return _libdrizzle.Column_charset(self)

    def size(self) -> 'uint32_t':
        return _libdrizzle.Column_size(self)

    def max_size(self) -> 'size_t':
        return _libdrizzle.Column_max_size(self)

    def type(self) -> 'drizzle_column_type_t':
        return _libdrizzle.Column_type(self)

    def flags(self) -> 'drizzle_column_flags_t':
        return _libdrizzle.Column_flags(self)

    def decimals(self) -> 'uint8_t':
        return _libdrizzle.Column_decimals(self)

    def default_value(self, *args) -> 'char *':
        return _libdrizzle.Column_default_value(self, *args)


Column_swigregister = _libdrizzle.Column_swigregister
Column_swigregister(Column)

class ColumnServer(Column):
    __swig_setmethods__ = {}
    for _s in [Column]:
        __swig_setmethods__.update(getattr(_s, '__swig_setmethods__', {}))

    __setattr__ = lambda self, name, value: _swig_setattr(self, ColumnServer, name, value)
    __swig_getmethods__ = {}
    for _s in [Column]:
        __swig_getmethods__.update(getattr(_s, '__swig_getmethods__', {}))

    __getattr__ = lambda self, name: _swig_getattr(self, ColumnServer, name)

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr

    def set_catalog(self, *args) -> 'void':
        return _libdrizzle.ColumnServer_set_catalog(self, *args)

    def set_db(self, *args) -> 'void':
        return _libdrizzle.ColumnServer_set_db(self, *args)

    def set_table(self, *args) -> 'void':
        return _libdrizzle.ColumnServer_set_table(self, *args)

    def set_orig_table(self, *args) -> 'void':
        return _libdrizzle.ColumnServer_set_orig_table(self, *args)

    def set_name(self, *args) -> 'void':
        return _libdrizzle.ColumnServer_set_name(self, *args)

    def set_orig_name(self, *args) -> 'void':
        return _libdrizzle.ColumnServer_set_orig_name(self, *args)

    def set_charset(self, *args) -> 'void':
        return _libdrizzle.ColumnServer_set_charset(self, *args)

    def set_size(self, *args) -> 'void':
        return _libdrizzle.ColumnServer_set_size(self, *args)

    def set_type(self, *args) -> 'void':
        return _libdrizzle.ColumnServer_set_type(self, *args)

    def set_flags(self, *args) -> 'void':
        return _libdrizzle.ColumnServer_set_flags(self, *args)

    def set_decimals(self, *args) -> 'void':
        return _libdrizzle.ColumnServer_set_decimals(self, *args)

    def set_default_value(self, *args) -> 'void':
        return _libdrizzle.ColumnServer_set_default_value(self, *args)

    __swig_destroy__ = _libdrizzle.delete_ColumnServer
    __del__ = lambda self: None


ColumnServer_swigregister = _libdrizzle.ColumnServer_swigregister
ColumnServer_swigregister(ColumnServer)