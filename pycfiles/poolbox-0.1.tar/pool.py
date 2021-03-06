# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/poolbase/pool.py
# Compiled at: 2014-03-19 10:58:00
__doc__ = '\nHappyBase connection pool module.\n'
import contextlib, logging, Queue, threading, socket
from .connection import Connection
logger = logging.getLogger(__name__)

class NoConnectionsAvailable(RuntimeError):
    """
Exception raised when no connections are available.

This happens if a timeout was specified when obtaining a connection,
and no connection became available within the specified timeout.

.. versionadded:: 0.5
"""


class ConnectionPool(object):
    """
Thread-safe connection pool.

.. versionadded:: 0.5

The `size` parameter specifies how many connections this pool
manages. Additional keyword arguments are passed unmodified to the
:py:class:`happybase.Connection` constructor, with the exception of
the `autoconnect` argument, since maintaining connections is the
task of the pool.

:param int size: the maximum number of concurrently open connections
:param kwargs: keyword arguments passed to
:py:class:`happybase.Connection`
"""

    def __init__(self, size, connection_klass=Connection, **kwargs):
        if not isinstance(size, int):
            raise TypeError("Pool 'size' arg must be an integer")
        if not size > 0:
            raise ValueError("Pool 'size' arg must be greater than zero")
        logger.debug('Initializing connection pool with %d connections', size)
        self._lock = threading.Lock()
        self._queue = Queue.LifoQueue(maxsize=size)
        self._thread_connections = threading.local()
        connection_kwargs = kwargs
        connection_kwargs['autoconnect'] = False
        for _ in xrange(size):
            connection = connection_klass(**connection_kwargs)
            self._queue.put(connection)

        with self.connection():
            pass

    def _acquire_connection(self, timeout=None):
        """Acquire a connection from the pool."""
        try:
            return self._queue.get(True, timeout)
        except Queue.Empty:
            raise NoConnectionsAvailable('No connection available from pool within specified timeout')

    def _return_connection(self, connection):
        """Return a connection to the pool."""
        self._queue.put(connection)

    @contextlib.contextmanager
    def connection(self, timeout=None):
        """
Obtain a connection from the pool.

This method *must* be used as a context manager, i.e. with
Python's ``with`` block. Example::

with pool.connection() as connection:
pass # do something with the connection

If `timeout` is specified, this is the number of seconds to wait
for a connection to become available before
:py:exc:`NoConnectionsAvailable` is raised. If omitted, this
method waits forever for a connection to become available.

:param int timeout: number of seconds to wait (optional)
:return: active connection from the pool
:rtype: :py:class:`happybase.Connection`
"""
        connection = getattr(self._thread_connections, 'current', None)
        return_after_use = False
        if connection is None:
            return_after_use = True
            connection = self._acquire_connection(timeout)
            with self._lock:
                self._thread_connections.current = connection
        try:
            try:
                connection.open()
                yield connection
            except BaseException as e:
                logger.exception(e)
                logger.info('Replacing tainted pool connection')
                connection.refresh()
                connection.open()
                raise

        finally:
            if return_after_use:
                del self._thread_connections.current
                self._return_connection(connection)

        return