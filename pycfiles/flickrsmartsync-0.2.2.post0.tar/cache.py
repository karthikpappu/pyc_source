# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/faisal/Developer/Projects/github/flickrsmartsync/flickrapi/cache.py
# Compiled at: 2014-06-18 08:36:36
"""Call result cache.

Designed to have the same interface as the `Django low-level cache API`_.
Heavily inspired (read: mostly copied-and-pasted) from the Django framework -
thanks to those guys for designing a simple and effective cache!

.. _`Django low-level cache API`: http://www.djangoproject.com/documentation/cache/#the-low-level-cache-api
"""
import threading, time

class SimpleCache(object):
    """Simple response cache for FlickrAPI calls.

    This stores max 50 entries, timing them out after 120 seconds:
    >>> cache = SimpleCache(timeout=120, max_entries=50)
    """

    def __init__(self, timeout=300, max_entries=200):
        self.storage = {}
        self.expire_info = {}
        self.lock = threading.RLock()
        self.default_timeout = timeout
        self.max_entries = max_entries
        self.cull_frequency = 3

    def locking(method):
        """Method decorator, ensures the method call is locked"""

        def locked(self, *args, **kwargs):
            self.lock.acquire()
            try:
                return method(self, *args, **kwargs)
            finally:
                self.lock.release()

        return locked

    @locking
    def get(self, key, default=None):
        """Fetch a given key from the cache. If the key does not exist, return
        default, which itself defaults to None.
        """
        now = time.time()
        exp = self.expire_info.get(key)
        if exp is None:
            return default
        else:
            if exp < now:
                self.delete(key)
                return default
            return self.storage[key]

    @locking
    def set(self, key, value, timeout=None):
        """Set a value in the cache. If timeout is given, that timeout will be
        used for the key; otherwise the default cache timeout will be used.
        """
        if len(self.storage) >= self.max_entries:
            self.cull()
        if timeout is None:
            timeout = self.default_timeout
        self.storage[key] = value
        self.expire_info[key] = time.time() + timeout
        return

    @locking
    def delete(self, key):
        """Deletes a key from the cache,
           failing silently if it doesn't exist."""
        if key in self.storage:
            del self.storage[key]
        if key in self.expire_info:
            del self.expire_info[key]

    @locking
    def has_key(self, key):
        """Returns True if the key is in the cache and has not expired."""
        return self.get(key) is not None

    @locking
    def __contains__(self, key):
        """Returns True if the key is in the cache and has not expired."""
        return self.has_key(key)

    @locking
    def cull(self):
        """Reduces the number of cached items"""
        doomed = [ k for i, k in enumerate(self.storage) if i % self.cull_frequency == 0
                 ]
        for k in doomed:
            self.delete(k)

    @locking
    def __len__(self):
        """Returns the number of cached items -- they might be expired
        though.
        """
        return len(self.storage)