# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aiothrottle\throttle.py
# Compiled at: 2016-08-27 08:11:46
# Size of source mod 2**32: 12542 bytes
"""
Throttle: Manages rate limiting for general connections
ThrottledStreamReader: Throttles aiohttp downloads
"""
import asyncio, aiohttp, logging, functools
LOGGER = logging.getLogger(__package__)

class Throttle:
    __doc__ = 'Throttle for IO operations\n\n    As soon as an IO action is registered using :meth:`add_io`,\n    :meth:`time_left` returns the seconds to wail until\n    ``[byte count] / [time passed] = [rate limit]``.\n    After that, :meth:`reset_io` has to be called to measure the new rate.\n\n    :param int limit: the limit in bytes to read/write per second\n    :raises: :class:`ValueError`: invalid rate given\n    '

    def __init__(self, limit, loop=None):
        self._limit = 0
        self.limit = limit
        self._io = 0
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._reset_time = loop.time()

    @property
    def limit(self):
        """
        :returns: the limit in bytes to read/write per second
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, value):
        """
        :param value: the limit in bytes to read/write per second
        :raises: :class:`ValueError` invalid rate given
        """
        if value <= 0:
            raise ValueError('rate_limit has to be greater than 0')
        self._limit = value

    def time_left(self):
        """returns the number of seconds left until the rate limit is reached

        :returns: seconds left until the rate limit is reached
        :rtype: float
        """
        remaining = self._io / self._limit
        LOGGER.debug('[throttle] time remaining: %.3f', remaining)
        return remaining

    def add_io(self, byte_count):
        """registers a number of bytes read/written

        :param int byte_count: number of bytes to add to the current rate
        """
        self._io += byte_count
        LOGGER.debug('[throttle] added bytes: %d, now: %d', byte_count, self._io)

    def reset_io(self):
        """resets the registered IO actions"""
        self._io = 0
        self._reset_time = self._loop.time()
        LOGGER.debug('[throttle] reset IO')

    @asyncio.coroutine
    def wait_remaining(self):
        """waits until the rate limit is reached"""
        time_left = self.time_left()
        LOGGER.debug('[throttle] sleeping for %.3f seconds', time_left)
        yield from asyncio.sleep(time_left)

    def current_rate(self):
        """returns the current rate, measured since :meth:`reset_io`

        In case the time since the last reset is too short,
        this returns ``-1``.

        :returns: the current rate in bytes per second
        :rtype: float
        """
        if self._io <= 0:
            return 0
        now = self._loop.time()
        duration = now - self._reset_time
        if duration <= 0:
            raise RuntimeError('unable to measure rate, duraction <= 0')
        rate = self._io / duration
        LOGGER.debug('[throttle] measured current rate: %.3f B/s', rate)
        return rate

    def within_limit(self):
        """returns the current limitation state

        :returns: ``True`` if the current rate is equal or below the limit rate
        :rtype: bool
        """
        current = self.current_rate()
        within_limit = current < self._limit
        LOGGER.debug('[throttle] %s rate', 'within' if within_limit else 'not within')
        return within_limit


class ThrottledStreamReader(aiohttp.StreamReader):
    __doc__ = 'Throttling, flow controlling :class:`aiohttp.streams.StreamReader`\n    for :meth:`aiohttp.request`\n\n    Usage:\n        >>> import functools\n        >>> import aiohttp\n        >>> import aiothrottle\n        >>> kbps = 200\n        >>> partial = functools.partial(\n        >>>     aiothrottle.ThrottledStreamReader, rate_limit=kbps * 1024)\n        >>> aiohttp.client_reqrep.ClientResponse.flow_control_class = partial\n\n    :param aiohttp.parsers.StreamParser stream: the base stream\n    :param int rate_limit: the rate limit in bytes per second\n    :param int buffer_limit: the internal buffer limit in bytes\n    :param asyncio.BaseEventLoop loop: the asyncio event loop\n    :param tuple args: arguments passed through to StreamReader\n    :param dict kwargs: keyword arguments passed through to StreamReader\n    '

    def __init__(self, stream, rate_limit, buffer_limit=65536, loop=None, *args, **kwargs):
        super().__init__(loop=loop, *args, **kwargs)
        self._loop = loop or asyncio.get_event_loop()
        self._throttle = Throttle(rate_limit, self._loop)
        self._stream = stream
        self._b_limit = buffer_limit * 2
        self._b_limit_reached = False
        self._check_handle = None
        self._throttling = True
        if stream.paused:
            try:
                stream.transport.resume_reading()
            except AttributeError:
                pass

    def __del__(self):
        if self._check_handle is not None:
            self._check_handle.cancel()

    @property
    def rate_limit(self):
        """
        :returns: the current rate limit
        :rtype: int

        .. versionadded:: 0.1.2
        """
        return self._throttle.limit

    @property
    def throttling(self):
        """
        :returns: wether the connection is being throttled
        :rtype: bool

        .. versionadded:: 0.1.2
        """
        return self._throttling

    def limit_rate(self, limit):
        """Sets the rate limit of this response

        :param limit: the limit in bytes to read/write per second

        .. versionadded:: 0.1.1
        """
        self._throttle.limit = limit
        self._throttling = True

    def unlimit_rate(self):
        """Unlimits the rate of this response

        .. versionadded:: 0.1.1
        """
        self._throttling = False
        if self._buffer_size < self._b_limit:
            self._try_resume()

    def _try_pause(self):
        """Pauses the transport if not already paused"""
        if self._stream.paused:
            return
        try:
            if self._stream.transport.is_closing():
                LOGGER.debug('[reader] is closing, not pausing')
                return
            self._stream.transport.pause_reading()
        except AttributeError:
            pass
        except RuntimeError as e:
            LOGGER.warn('[reader] RuntimeError: %s', e)
        else:
            self._stream.paused = True
            LOGGER.debug('[reader] paused')

    def _try_resume(self):
        """Resumed the transport if paused"""
        if not self._stream.paused:
            return
        try:
            self._stream.transport.resume_reading()
        except AttributeError:
            pass
        else:
            self._stream.paused = False
            LOGGER.debug('[reader] resumed')

    def feed_data(self, data, _=0):
        """Feeds data into the internal buffer"""
        LOGGER.debug('[reader] got fed %d bytes', len(data))
        super().feed_data(data)
        self._throttle.reset_io()
        self._throttle.add_io(len(data))
        self._check_limits()

    def _check_callback(self):
        """Tries to resume the transport after the rate limit is reached"""
        self._check_handle = None
        self._try_resume()

    def _schedule_resume(self):
        """resumes the transport as soon as the rate limit is reached"""
        if self._check_handle is not None:
            self._check_handle.cancel()
        pause_time = self._throttle.time_left()
        LOGGER.debug('[reader] resuming in %.3f seconds', pause_time)
        self._check_handle = self._loop.call_later(pause_time, self._check_callback)

    @asyncio.coroutine
    def _check_buffer_limit(self):
        """Controls the size of the internal buffer"""
        buf_size = self._buffer_size
        if self._stream.paused:
            try:
                within_limit = self._throttle.within_limit()
            except RuntimeError:
                yield from asyncio.sleep(0.001)
                yield from self._check_buffer_limit()
                return

            resume = buf_size < self._b_limit and (not self._throttling or within_limit)
            if resume:
                LOGGER.debug('[reader] resuming throttling')
                self._try_resume()
                self._b_limit_reached = False
            else:
                self._schedule_resume()
        elif not buf_size <= self._b_limit:
            raise AssertionError

    def _check_limits(self):
        """Controls rate and buffer size by pausing/resuming the transport"""
        if self._check_handle is not None:
            self._check_handle.cancel()
            self._check_handle = None
        buf_size = self._buffer_size
        if not self._throttling:
            if self._stream.paused:
                if buf_size < self._b_limit:
                    LOGGER.debug('[reader] resuming unthrottling')
                    self._try_resume()
            return
        self._try_pause()
        if buf_size >= self._b_limit:
            LOGGER.debug('[reader] byte limit reached, not resuming')
            self._b_limit_reached = True
            return
        self._schedule_resume()

    @asyncio.coroutine
    def read(self, byte_count=-1):
        """Reads at most the requested number of bytes from the internal buffer

        :param int byte_count: the number of bytes to read
        :returns: the data
        :rtype: bytes
        """
        LOGGER.debug('[reader] reading %d bytes', byte_count)
        data = yield from super().read(byte_count)
        yield from self._check_buffer_limit()
        return data

    @asyncio.coroutine
    def readline(self):
        r"""Reads bytes from the internal buffer until ``\n`` is found

        :returns: the data
        :rtype: bytes
        """
        LOGGER.debug('[reader] reading line')
        data = yield from super().readline()
        yield from self._check_buffer_limit()
        return data

    @asyncio.coroutine
    def readany(self):
        """Reads the bytes next received from the internal buffer

        :returns: the data
        :rtype: bytes
        """
        LOGGER.debug('[reader] reading anything')
        data = yield from super().readany()
        yield from self._check_buffer_limit()
        return data

    @asyncio.coroutine
    def readexactly(self, byte_count):
        """Reads the requested number of bytes from the internal buffer

        This raises :class:`asyncio.IncompleteReadError` if
        the stream ended before enough bytes were received

        :param int byte_count: the number of bytes to read
        :returns: the data
        :rtype: bytes
        """
        LOGGER.debug('[reader] reading exactly %d bytes', byte_count)
        data = yield from super().readexactly(byte_count)
        yield from self._check_buffer_limit()
        return data


def limit_rate(limit):
    """Limits the rate of all subsequent aiohttp requests

    :param limit: the limit in bytes to read/write per second

    .. versionadded:: 0.1.1
    """
    partial = functools.partial(ThrottledStreamReader, rate_limit=limit)
    aiohttp.client_reqrep.ClientResponse.flow_control_class = partial


def unlimit_rate():
    """Unlimits the rate of all subsequent aiohttp requests

    .. versionadded:: 0.1.1
    """
    aiohttp.client_reqrep.ClientResponse.flow_control_class = aiohttp.streams.FlowControlStreamReader