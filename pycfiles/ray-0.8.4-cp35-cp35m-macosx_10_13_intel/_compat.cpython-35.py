# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/nz/vv4_9tw56nv9k3tkvyszvwg80000gn/T/pip-unpacked-wheel-_x_fz5x6/psutil/_compat.py
# Compiled at: 2020-04-01 16:57:58
# Size of source mod 2**32: 11607 bytes
"""Module which provides compatibility with older Python versions."""
import collections, errno, functools, os, sys
__all__ = [
 'PY3', 'long', 'xrange', 'unicode', 'basestring', 'u', 'b',
 'lru_cache', 'which', 'get_terminal_size',
 'FileNotFoundError', 'PermissionError', 'ProcessLookupError',
 'InterruptedError', 'ChildProcessError', 'FileExistsError']
PY3 = sys.version_info[0] == 3
if PY3:
    long = int
    xrange = range
    unicode = str
    basestring = str

    def u(s):
        return s


    def b(s):
        return s.encode('latin-1')


else:
    long = long
    xrange = xrange
    unicode = unicode
    basestring = basestring

    def u(s):
        return unicode(s, 'unicode_escape')


    def b(s):
        return s


if PY3:
    FileNotFoundError = FileNotFoundError
    PermissionError = PermissionError
    ProcessLookupError = ProcessLookupError
    InterruptedError = InterruptedError
    ChildProcessError = ChildProcessError
    FileExistsError = FileExistsError
else:
    import platform
    _singleton = object()

    def instance_checking_exception(base_exception=Exception):

        def wrapped(instance_checker):

            class TemporaryClass(base_exception):

                def __init__(self, *args, **kwargs):
                    if len(args) == 1 and isinstance(args[0], TemporaryClass):
                        unwrap_me = args[0]
                        for attr in dir(unwrap_me):
                            if not attr.startswith('__'):
                                setattr(self, attr, getattr(unwrap_me, attr))

                    else:
                        super(TemporaryClass, self).__init__(*args, **kwargs)

                class __metaclass__(type):

                    def __instancecheck__(cls, inst):
                        return instance_checker(inst)

                    def __subclasscheck__(cls, classinfo):
                        value = sys.exc_info()[1]
                        return isinstance(value, cls)

            TemporaryClass.__name__ = instance_checker.__name__
            TemporaryClass.__doc__ = instance_checker.__doc__
            return TemporaryClass

        return wrapped


    @instance_checking_exception(EnvironmentError)
    def FileNotFoundError(inst):
        return getattr(inst, 'errno', _singleton) == errno.ENOENT


    @instance_checking_exception(EnvironmentError)
    def ProcessLookupError(inst):
        return getattr(inst, 'errno', _singleton) == errno.ESRCH


    @instance_checking_exception(EnvironmentError)
    def PermissionError(inst):
        return getattr(inst, 'errno', _singleton) in (
         errno.EACCES, errno.EPERM)


    @instance_checking_exception(EnvironmentError)
    def InterruptedError(inst):
        return getattr(inst, 'errno', _singleton) == errno.EINTR


    @instance_checking_exception(EnvironmentError)
    def ChildProcessError(inst):
        return getattr(inst, 'errno', _singleton) == errno.ECHILD


    @instance_checking_exception(EnvironmentError)
    def FileExistsError(inst):
        return getattr(inst, 'errno', _singleton) == errno.EEXIST


if platform.python_implementation() != 'CPython':
    try:
        raise OSError(errno.EEXIST, 'perm')
    except FileExistsError:
        pass
    except OSError:
        raise RuntimeError('broken / incompatible Python implementation, see: https://github.com/giampaolo/psutil/issues/1659')

try:
    from functools import lru_cache
except ImportError:
    try:
        from threading import RLock
    except ImportError:
        from dummy_threading import RLock

    _CacheInfo = collections.namedtuple('CacheInfo', ['hits', 'misses', 'maxsize', 'currsize'])

    class _HashedSeq(list):
        __slots__ = 'hashvalue'

        def __init__(self, tup, hash=hash):
            self[:] = tup
            self.hashvalue = hash(tup)

        def __hash__(self):
            return self.hashvalue


    def _make_key(args, kwds, typed, kwd_mark=(
 object(),), fasttypes=set((int, str, frozenset, type(None))), sorted=sorted, tuple=tuple, type=type, len=len):
        key = args
        if kwds:
            sorted_items = sorted(kwds.items())
            key += kwd_mark
            for item in sorted_items:
                key += item

        if typed:
            key += tuple(type(v) for v in args)
            if kwds:
                key += tuple(type(v) for k, v in sorted_items)
        elif len(key) == 1 and type(key[0]) in fasttypes:
            return key[0]
        return _HashedSeq(key)


    def lru_cache(maxsize=100, typed=False):
        """Least-recently-used cache decorator, see:
        http://docs.python.org/3/library/functools.html#functools.lru_cache
        """

        def decorating_function(user_function):
            cache = dict()
            stats = [0, 0]
            HITS, MISSES = (0, 1)
            make_key = _make_key
            cache_get = cache.get
            _len = len
            lock = RLock()
            root = []
            root[:] = [root, root, None, None]
            nonlocal_root = [root]
            PREV, NEXT, KEY, RESULT = (0, 1, 2, 3)
            if maxsize == 0:

                def wrapper(*args, **kwds):
                    result = user_function(*args, **kwds)
                    stats[MISSES] += 1
                    return result

            else:
                if maxsize is None:

                    def wrapper(*args, **kwds):
                        key = make_key(args, kwds, typed)
                        result = cache_get(key, root)
                        if result is not root:
                            stats[HITS] += 1
                            return result
                        result = user_function(*args, **kwds)
                        cache[key] = result
                        stats[MISSES] += 1
                        return result

                else:

                    def wrapper(*args, **kwds):
                        if kwds or typed:
                            key = make_key(args, kwds, typed)
                        else:
                            key = args
                        lock.acquire()
                        try:
                            link = cache_get(key)
                            if link is not None:
                                root, = nonlocal_root
                                link_prev, link_next, key, result = link
                                link_prev[NEXT] = link_next
                                link_next[PREV] = link_prev
                                last = root[PREV]
                                last[NEXT] = root[PREV] = link
                                link[PREV] = last
                                link[NEXT] = root
                                stats[HITS] += 1
                                return result
                        finally:
                            lock.release()

                        result = user_function(*args, **kwds)
                        lock.acquire()
                        try:
                            root, = nonlocal_root
                            if key in cache:
                                pass
                            else:
                                if _len(cache) >= maxsize:
                                    oldroot = root
                                    oldroot[KEY] = key
                                    oldroot[RESULT] = result
                                    root = nonlocal_root[0] = oldroot[NEXT]
                                    oldkey = root[KEY]
                                    root[KEY] = root[RESULT] = None
                                    del cache[oldkey]
                                    cache[key] = oldroot
                                else:
                                    last = root[PREV]
                                    link = [last, root, key, result]
                                    last[NEXT] = root[PREV] = cache[key] = link
                            stats[MISSES] += 1
                        finally:
                            lock.release()

                        return result

            def cache_info():
                """Report cache statistics"""
                lock.acquire()
                try:
                    return _CacheInfo(stats[HITS], stats[MISSES], maxsize, len(cache))
                finally:
                    lock.release()

            def cache_clear():
                """Clear the cache and cache statistics"""
                lock.acquire()
                try:
                    cache.clear()
                    root = nonlocal_root[0]
                    root[:] = [root, root, None, None]
                    stats[:] = [0, 0]
                finally:
                    lock.release()

            wrapper.__wrapped__ = user_function
            wrapper.cache_info = cache_info
            wrapper.cache_clear = cache_clear
            return functools.update_wrapper(wrapper, user_function)

        return decorating_function


try:
    from shutil import which
except ImportError:

    def which(cmd, mode=os.F_OK | os.X_OK, path=None):
        """Given a command, mode, and a PATH string, return the path which
        conforms to the given mode on the PATH, or None if there is no such
        file.

        `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
        of os.environ.get("PATH"), or can be overridden with a custom search
        path.
        """

        def _access_check(fn, mode):
            return os.path.exists(fn) and os.access(fn, mode) and not os.path.isdir(fn)

        if os.path.dirname(cmd):
            if _access_check(cmd, mode):
                return cmd
            return
        if path is None:
            path = os.environ.get('PATH', os.defpath)
        if not path:
            return
        path = path.split(os.pathsep)
        if sys.platform == 'win32':
            if os.curdir not in path:
                path.insert(0, os.curdir)
            pathext = os.environ.get('PATHEXT', '').split(os.pathsep)
            if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
                files = [
                 cmd]
            else:
                files = [cmd + ext for ext in pathext]
        else:
            files = [
             cmd]
        seen = set()
        for dir in path:
            normdir = os.path.normcase(dir)
            if normdir not in seen:
                seen.add(normdir)
                for thefile in files:
                    name = os.path.join(dir, thefile)
                    if _access_check(name, mode):
                        return name


try:
    from shutil import get_terminal_size
except ImportError:

    def get_terminal_size(fallback=(80, 24)):
        try:
            import fcntl, termios, struct
        except ImportError:
            return fallback
        else:
            try:
                res = struct.unpack('hh', fcntl.ioctl(1, termios.TIOCGWINSZ, '1234'))
                return (res[1], res[0])
            except Exception:
                return fallback