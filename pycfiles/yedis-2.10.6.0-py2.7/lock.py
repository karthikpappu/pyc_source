# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/yedis/lock.py
# Compiled at: 2018-10-31 18:35:23
import threading, time as mod_time, uuid
from redis.exceptions import LockError, WatchError
from redis.utils import dummy
from redis._compat import b

class Lock(object):
    """
    A shared, distributed Lock. Using Redis for locking allows the Lock
    to be shared across processes and/or machines.

    It's left to the user to resolve deadlock issues and make sure
    multiple clients play nicely together.
    """

    def __init__(self, redis, name, timeout=None, sleep=0.1, blocking=True, blocking_timeout=None, thread_local=True):
        """
        Create a new Lock instance named ``name`` using the Redis client
        supplied by ``redis``.

        ``timeout`` indicates a maximum life for the lock.
        By default, it will remain locked until release() is called.
        ``timeout`` can be specified as a float or integer, both representing
        the number of seconds to wait.

        ``sleep`` indicates the amount of time to sleep per loop iteration
        when the lock is in blocking mode and another client is currently
        holding the lock.

        ``blocking`` indicates whether calling ``acquire`` should block until
        the lock has been acquired or to fail immediately, causing ``acquire``
        to return False and the lock not being acquired. Defaults to True.
        Note this value can be overridden by passing a ``blocking``
        argument to ``acquire``.

        ``blocking_timeout`` indicates the maximum amount of time in seconds to
        spend trying to acquire the lock. A value of ``None`` indicates
        continue trying forever. ``blocking_timeout`` can be specified as a
        float or integer, both representing the number of seconds to wait.

        ``thread_local`` indicates whether the lock token is placed in
        thread-local storage. By default, the token is placed in thread local
        storage so that a thread only sees its token, not a token set by
        another thread. Consider the following timeline:

            time: 0, thread-1 acquires `my-lock`, with a timeout of 5 seconds.
                     thread-1 sets the token to "abc"
            time: 1, thread-2 blocks trying to acquire `my-lock` using the
                     Lock instance.
            time: 5, thread-1 has not yet completed. redis expires the lock
                     key.
            time: 5, thread-2 acquired `my-lock` now that it's available.
                     thread-2 sets the token to "xyz"
            time: 6, thread-1 finishes its work and calls release(). if the
                     token is *not* stored in thread local storage, then
                     thread-1 would see the token value as "xyz" and would be
                     able to successfully release the thread-2's lock.

        In some use cases it's necessary to disable thread local storage. For
        example, if you have code where one thread acquires a lock and passes
        that lock instance to a worker thread to release later. If thread
        local storage isn't disabled in this case, the worker thread won't see
        the token set by the thread that acquired the lock. Our assumption
        is that these cases aren't common and as such default to using
        thread local storage.
        """
        self.redis = redis
        self.name = name
        self.timeout = timeout
        self.sleep = sleep
        self.blocking = blocking
        self.blocking_timeout = blocking_timeout
        self.thread_local = bool(thread_local)
        self.local = threading.local() if self.thread_local else dummy()
        self.local.token = None
        if self.timeout and self.sleep > self.timeout:
            raise LockError("'sleep' must be less than 'timeout'")
        return

    def __enter__(self):
        self.acquire(blocking=True)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    def acquire(self, blocking=None, blocking_timeout=None):
        """
        Use Redis to hold a shared, distributed lock named ``name``.
        Returns True once the lock is acquired.

        If ``blocking`` is False, always return immediately. If the lock
        was acquired, return True, otherwise return False.

        ``blocking_timeout`` specifies the maximum number of seconds to
        wait trying to acquire the lock.
        """
        sleep = self.sleep
        token = b(uuid.uuid1().hex)
        if blocking is None:
            blocking = self.blocking
        if blocking_timeout is None:
            blocking_timeout = self.blocking_timeout
        stop_trying_at = None
        if blocking_timeout is not None:
            stop_trying_at = mod_time.time() + blocking_timeout
        while 1:
            if self.do_acquire(token):
                self.local.token = token
                return True
            if not blocking:
                return False
            if stop_trying_at is not None and mod_time.time() > stop_trying_at:
                return False
            mod_time.sleep(sleep)

        return

    def do_acquire(self, token):
        if self.timeout:
            timeout = int(self.timeout * 1000)
        else:
            timeout = None
        if self.redis.set(self.name, token, nx=True, px=timeout):
            return True
        else:
            return False

    def release(self):
        """Releases the already acquired lock"""
        expected_token = self.local.token
        if expected_token is None:
            raise LockError('Cannot release an unlocked lock')
        self.local.token = None
        self.do_release(expected_token)
        return

    def do_release(self, expected_token):
        name = self.name

        def execute_release(pipe):
            lock_value = pipe.get(name)
            if lock_value != expected_token:
                raise LockError("Cannot release a lock that's no longer owned")
            pipe.delete(name)

        self.redis.transaction(execute_release, name)

    def extend(self, additional_time):
        """
        Adds more time to an already acquired lock.

        ``additional_time`` can be specified as an integer or a float, both
        representing the number of seconds to add.
        """
        if self.local.token is None:
            raise LockError('Cannot extend an unlocked lock')
        if self.timeout is None:
            raise LockError('Cannot extend a lock with no timeout')
        return self.do_extend(additional_time)

    def do_extend(self, additional_time):
        pipe = self.redis.pipeline()
        pipe.watch(self.name)
        lock_value = pipe.get(self.name)
        if lock_value != self.local.token:
            raise LockError("Cannot extend a lock that's no longer owned")
        expiration = pipe.pttl(self.name)
        if expiration is None or expiration < 0:
            expiration = 0
        pipe.multi()
        pipe.pexpire(self.name, expiration + int(additional_time * 1000))
        try:
            response = pipe.execute()
        except WatchError:
            raise LockError("Cannot extend a lock that's no longer owned")

        if not response[0]:
            raise LockError("Cannot extend a lock that's no longer owned")
        return True


class LuaLock(Lock):
    """
    A lock implementation that uses Lua scripts rather than pipelines
    and watches.
    """
    lua_release = None
    lua_extend = None
    LUA_RELEASE_SCRIPT = "\n        local token = redis.call('get', KEYS[1])\n        if not token or token ~= ARGV[1] then\n            return 0\n        end\n        redis.call('del', KEYS[1])\n        return 1\n    "
    LUA_EXTEND_SCRIPT = "\n        local token = redis.call('get', KEYS[1])\n        if not token or token ~= ARGV[1] then\n            return 0\n        end\n        local expiration = redis.call('pttl', KEYS[1])\n        if not expiration then\n            expiration = 0\n        end\n        if expiration < 0 then\n            return 0\n        end\n        redis.call('pexpire', KEYS[1], expiration + ARGV[2])\n        return 1\n    "

    def __init__(self, *args, **kwargs):
        super(LuaLock, self).__init__(*args, **kwargs)
        LuaLock.register_scripts(self.redis)

    @classmethod
    def register_scripts(cls, redis):
        if cls.lua_release is None:
            cls.lua_release = redis.register_script(cls.LUA_RELEASE_SCRIPT)
        if cls.lua_extend is None:
            cls.lua_extend = redis.register_script(cls.LUA_EXTEND_SCRIPT)
        return

    def do_release(self, expected_token):
        if not bool(self.lua_release(keys=[self.name], args=[
         expected_token], client=self.redis)):
            raise LockError("Cannot release a lock that's no longer owned")

    def do_extend(self, additional_time):
        additional_time = int(additional_time * 1000)
        if not bool(self.lua_extend(keys=[self.name], args=[
         self.local.token, additional_time], client=self.redis)):
            raise LockError("Cannot extend a lock that's no longer owned")
        return True