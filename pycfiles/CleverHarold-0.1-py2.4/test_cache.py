# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/harold/tests/test_cache.py
# Compiled at: 2006-08-02 05:57:50
""" Tests for harold.cache

"""
import time, unittest
from harold.cache import CacheMiddleware, cacheable
from harold.tests.lib import wsgi_env, make_start_response
test_default_ttl = 0.5

def monkey_patch_cache_ttl():
    from harold.cache import lib
    lib.default_ttl = test_default_ttl


monkey_patch_cache_ttl()
cacheable_urls = [
 dict(pattern='/foo'), dict(pattern='/boo', ttl=0), dict(pattern='/bar/.*', keys='REMOTE_USER'), dict(pattern='/baz/eggs/.*?/spam', keys=('REMOTE_USER', 'REMOTE_ADDR'))]

def snooze(value=None):
    amount = (value is None and test_default_ttl or value) + 0.1
    time.sleep(amount)
    return


class TestApp:
    __module__ = __name__

    def __init__(self):
        self.created = time.time()

    def __call__(self, environ, start_response):
        return [
         time.time()]


class CacheResultsTest(unittest.TestCase):
    __module__ = __name__

    def test_one_call(self):
        """ test only one call to a cached function """

        @cacheable()
        def X():
            return time.time()

        counters = X.cache.counters
        self.assertAlmostEqual(X(), X())
        self.assertEqual(counters['missed'], 1)
        self.assertEqual(counters['hit'], 1)

    def test_langoliers(self):
        """ test langoleirs clearing cached items """

        @cacheable(ttl=1)
        def X(a):
            return (a, time.time())

        counters = X.cache.counters
        results = [ X(b) for b in range(10) ]
        self.assertEqual(counters['missed'], 10)
        self.assertEqual(counters['hit'], 0)
        snooze(5)
        self.assertEqual(counters['cleared'], 10)


def dummy_start_response(status, headers, exc=None):
    pass


class CacheMiddlewareTest(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.test_app = CacheMiddleware(TestApp(), cacheable_urls)

    def test_one_call(self):
        """ test only one call to cached middleware """
        app = self.test_app
        env = wsgi_env()
        val = app(env, dummy_start_response)[0]
        self.failUnless(val > app.app.created)

    def test_miss_hit(self):
        """ test cache miss and hit """
        app = self.test_app
        env = wsgi_env(SCRIPT_NAME='/foo')
        miss = app(env, dummy_start_response)[0]
        hit = app(env, dummy_start_response)[0]
        counters = app.counters
        self.assertAlmostEqual(miss, hit)
        self.assertEqual(counters['missed'], 1)
        self.assertEqual(counters['hit'], 1)

    def test_miss_miss(self):
        """ test cache entry invalidation """
        app = self.test_app
        env = wsgi_env(SCRIPT_NAME='/foo')
        miss = app(env, dummy_start_response)[0]
        counters = app.counters
        self.assertEqual(counters['missed'], 1)
        snooze()
        another = app(env, dummy_start_response)[0]
        self.failUnless(another > miss)
        self.assertEqual(counters['missed'], 2)
        self.assertEqual(counters['cleared'], 1)

    def test_miss_hit_no_expire(self):
        """ test miss and hit on not invalid """
        app = self.test_app
        env = wsgi_env(SCRIPT_NAME='/boo')
        miss = app(env, dummy_start_response)[0]
        counters = app.counters
        self.assertEqual(counters['missed'], 1)
        self.assertEqual(counters['hit'], 0)
        snooze()
        another = app(env, dummy_start_response)[0]
        self.assertAlmostEqual(miss, another)
        self.assertEqual(counters['hit'], 1)
        self.assertEqual(counters['missed'], 1)
        self.assertEqual(counters['cleared'], 0)


if __name__ == '__main__':
    unittest.main()