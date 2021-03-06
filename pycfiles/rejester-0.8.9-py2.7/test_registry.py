# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rejester/tests/test_registry.py
# Compiled at: 2015-07-08 07:32:10
"""

"""
from __future__ import absolute_import
from collections import defaultdict
import logging, os, sys, time, pytest, rejester
from rejester.exceptions import EnvironmentError, LockError
logger = logging.getLogger(__name__)
pytest_plugins = 'rejester.tests.fixtures'

def test_registry_decode(registry):
    for foo in [{}, None, '', 0, 1]:
        assert registry._decode(registry._encode(foo)) == foo

    return


def test_registry_lock_block(registry):
    with registry.lock(ltime=100) as (session1):
        with pytest.raises(rejester.exceptions.LockError):
            with registry.lock(atime=1) as (session2):
                pass


def test_registry_lock_loss(registry, registry2):
    with pytest.raises(LockError) as (env_error):
        with registry.lock(ltime=1) as (session1):
            with registry2.lock(atime=100) as (session2):
                assert session2
            session1.filter('x')


def test_registry_re_acquire_lock(registry, registry2):
    with registry.lock(ltime=1000) as (session):
        assert session.re_acquire_lock(ltime=1)
        with registry2.lock(atime=10) as (session2):
            assert session2
        with pytest.raises(EnvironmentError):
            session.re_acquire_lock()


def test_registry_update_pull(registry):
    test_dict = dict(cars=10, houses=5)
    with registry.lock() as (session):
        session.update('test_dict', test_dict)
        assert session.pull('test_dict') == test_dict


def test_registry_filter(registry):
    test_dict = dict(cars=10, houses=5)
    with registry.lock() as (session):
        session.update('test_dict', test_dict, priorities=dict(cars=100, houses=-100))
        assert session.filter('test_dict') == test_dict
        assert session.filter('test_dict', priority_min=0) == dict(cars=10)
        assert session.filter('test_dict', priority_max=0) == dict(houses=5)


def test_registry_update_expire(registry):
    test_dict = dict(cars=10, houses=5)
    with registry.lock(atime=5000) as (session):
        session.update('test_dict', test_dict, expire=2)
        assert session.pull('test_dict') == test_dict
        time.sleep(3)
        assert session.pull('darn') == {}
        assert session.pull('test_dict') == {}


def test_registry_get(registry):
    test_dict = dict(cars=10, houses=5)
    with registry.lock(atime=5000) as (session):
        session.update('test_dict', test_dict)
        assert session.pull('test_dict') == test_dict
        assert session.get('test_dict', 'cars') == 10
        assert session.get('test_dict', 'not-there', 'hello') == 'hello'


def test_registry_set(registry):
    test_dict = dict(cars=10, houses=5)
    with registry.lock(atime=5000) as (session):
        session.set('test_dict', 'cars', 10)
        session.set('test_dict', 'houses', 5)
        assert session.pull('test_dict') == test_dict


def test_registry_set_priority(registry):
    with registry.lock(atime=5000) as (session):
        session.set('test_dict', 'cars', 10, 100)
        assert session.popitem('test_dict', priority_max=0) is None
        assert session.popitem('test_dict', priority_max=200) == ('cars', 10)
    return


def test_registry_delete(registry):
    test_dict = dict(cars=10, houses=5)
    with registry.lock(atime=5000) as (session):
        session.set('test_dict', 'cars', 10)
        session.set('test_dict', 'houses', 5)
        assert session.pull('test_dict') == test_dict
        session.delete('test_dict')
        assert session.pull('test_dict') == {}
        assert session.popitem('test_dict') is None
    return


def test_registry_popmany(registry):
    test_dict = dict(cars=10, houses=5)
    with registry.lock(atime=5000) as (session):
        session.update('test_dict', test_dict)
        assert session.pull('test_dict') == test_dict
        session.popmany('test_dict', 'dogs', 'cars', 'houses')
        assert session.pull('test_dict') == dict()


def test_registry_popitem(registry):
    test_dict = dict(cars=10, houses=5)
    recovered = set()
    with registry.lock(atime=5000) as (session):
        session.update('test_dict', test_dict)
        assert session.pull('test_dict') == test_dict
        recovered.add(session.popitem('test_dict'))
        recovered.add(session.popitem('test_dict'))
        assert recovered == set(test_dict.items())
        assert session.popitem('test_dict') is None
    return


def test_registry_popitem_priority(registry):
    test_dict = dict(cars=10, houses=5, dogs=99)
    recovered = set()
    with registry.lock(atime=5000) as (session):
        session.update('test_dict', test_dict, priorities=defaultdict(lambda : 10))
        assert session.pull('test_dict') == test_dict
        assert session.popitem('test_dict', priority_min=100) is None
        recovered.add(session.popitem('test_dict', priority_min=-100))
        recovered.add(session.popitem('test_dict', priority_min=10))
        recovered.add(session.popitem('test_dict'))
        assert recovered == set(test_dict.items())
    return


def test_registry_popitem_move(registry):
    test_dict = dict(cars=10, houses=5)
    recovered = set()
    with registry.lock(atime=5000) as (session):
        session.update('test_dict', test_dict)
        assert session.pull('test_dict') == test_dict
        recovered.add(session.popitem_move('test_dict', 'second'))
        assert session.len('test_dict') == 1
        assert session.len('second') == 1
        recovered.add(session.popitem_move('test_dict', 'second'))
        assert session.len('test_dict') == 0
        assert session.len('second') == 2
        assert recovered == set(test_dict.items())
        assert recovered == set(session.pull('second').items())


def test_registry_popitem_move_all(registry):
    test_dict = dict(cars=10, houses=5)
    recovered = set()
    with registry.lock(atime=5000) as (session):
        session.update('test_dict', test_dict, priorities=defaultdict(lambda : 100))
        session.move_all('test_dict', 'second')
        assert session.popitem('second', priority_max=0) is None
        assert session.pull('second') == test_dict
        assert session.len('test_dict') == 0
    return


def test_registry_popitem_move_priority(registry):
    test_dict = dict(cars=10, houses=5, dogs=99)
    recovered = set()
    with registry.lock(atime=5000) as (session):
        session.update('test_dict', test_dict, priorities=defaultdict(lambda : 10))
        assert session.pull('test_dict') == test_dict
        assert session.popitem_move('test_dict', 'second', priority_min=100) is None
        assert session.popitem_move('test_dict', 'second', priority_max=-100) is None
        recovered.add(session.popitem_move('test_dict', 'second', priority_min=-100))
        recovered.add(session.popitem_move('test_dict', 'second', priority_min=10))
        recovered.add(session.popitem_move('test_dict', 'second'))
        assert recovered == set(test_dict.items())
        assert recovered == set(session.pull('second').items())
    return


def test_registry_popitem_move_empty(registry):
    test_dict = dict(cars=10, houses=5)
    recovered = set()
    with registry.lock(atime=5000) as (session):
        session.update('test_dict', test_dict)
        assert session.pull('test_dict') == test_dict
        session.popitem_move('test_dict', 'second')
        session.popitem_move('test_dict', 'second')
        assert session.len('test_dict') == 0
        assert session.popitem_move('test_dict', 'second') is None
    return


def test_registry_move(registry):
    test_dict = dict(cars=10, houses=5, dogs=4)
    recovered = set()
    with registry.lock(atime=5000) as (session):
        session.update('test_dict', test_dict)
        assert session.pull('test_dict') == test_dict
        assert session.len('test_dict') == 3
        session.move('test_dict', 'second', dict(cars=3))
        assert session.len('test_dict') == 2
        assert session.len('second') == 1
        session.move('test_dict', 'second', dict(houses=2))
        assert session.len('test_dict') == 1
        assert session.len('second') == 2
        assert dict(cars=3, houses=2) == session.pull('second')
        assert dict(dogs=4) == session.pull('test_dict')


def test_registry_getitem_reset_priorities(registry):
    test_dict = dict(cars=10, houses=5)
    with registry.lock() as (session):
        session.update('test_dict', test_dict)
        assert session.pull('test_dict') == test_dict
        session.reset_priorities('test_dict', -100)
        assert session.popitem('test_dict', priority_min=0) is None
        assert session.popitem('test_dict', priority_min=-100)
        assert session.popitem('test_dict', priority_min=-100)
    return


def test_registry_getitem_reset(registry):
    test_dict = dict(cars=10, houses=5)
    recovered1 = set()
    recovered2 = set()
    with registry.lock(atime=5000) as (session):
        session.update('test_dict', test_dict)
        assert session.pull('test_dict') == test_dict
        assert session.getitem_reset('test_dict', priority_min=10) is None
        recovered1.add(session.getitem_reset('test_dict', priority_min=-10, new_priority=10))
        recovered1.add(session.getitem_reset('test_dict', priority_min=-10, priority_max=8, new_priority=10))
        assert recovered1 == set(test_dict.items())
        assert session.getitem_reset('test_dict', priority_max=9) is None
        recovered2.add(session.getitem_reset('test_dict', priority_max=10, new_priority=20))
        recovered2.add(session.getitem_reset('test_dict', priority_max=10))
        assert recovered2 == set(test_dict.items())
    return


def test_registry_1to1(registry):
    with registry.lock() as (session):
        session.set_1to1('test_dict', 'k1', 'v1')
        assert session.get('test_dict', 'k1') == 'v1'
        assert session.get('test_dict', 'v1') == 'k1'
        session.set_1to1('test_dict', 'v1', 'k3')
        assert session.get('test_dict', 'k3') == 'v1'
        assert session.get('test_dict', 'v1') == 'k3'


def test_registry_update_locks(registry):
    test_dict = dict(dog=10, cat=42)
    test_locks = dict(dog='w1', cat='w3')
    with registry.lock() as (session):
        session.update('test_dict', test_dict, locks=test_locks)
        assert session.pull('test_dict') == test_dict
        session.update('test_dict', dict(dog=4), locks=dict(dog='w1'))
        assert session.get('test_dict', 'dog') == 4
        with pytest.raises(EnvironmentError):
            session.update('test_dict', dict(dog=8), locks=dict(dog='w3'))
        assert session.get('test_dict', 'dog') == 4


def test_registry_getitem_reset_lock(registry):
    test_dict = dict(cars=10, houses=5)
    with registry.lock() as (session):
        session.update('test_dict', test_dict)
        assert session.pull('test_dict') == test_dict
        k1, v1 = session.getitem_reset('test_dict', lock='w1', new_priority=100)
        k3, v3 = session.getitem_reset('test_dict', lock='w3', priority_max=100)
        logger.info({k1: v1, k3: v3})
        logger.info(session.pull('test_dict_locks'))
        good_locks = {k1: 'w1', k3: 'w3', 'w1': k1, 'w3': k3}
        bad_locks = {k1: 'w1-', k3: 'w3', 'w1-': k1, 'w3': k3}
        assert good_locks == session.pull('test_dict_locks')
        assert bad_locks != session.pull('test_dict_locks')
        logger.info('good_locks: %r, bad_locks: %r', good_locks, bad_locks)
        session.update('test_dict', mapping=test_dict, locks=good_locks)
        with pytest.raises(EnvironmentError):
            session.update('test_dict', mapping=test_dict, locks={k1: 'w1-', k3: 'w3'})


def test_registry_getitem_reset_lock_1to1(registry):
    test_dict = dict(cars=10, houses=5)
    with registry.lock() as (session):
        session.update('test_dict', test_dict)
        assert session.pull('test_dict') == test_dict
        k1, v1 = session.getitem_reset('test_dict', lock='w1', new_priority=100)
        k3, v3 = session.getitem_reset('test_dict', lock='w3', priority_max=100)
        locks = session.pull('test_dict_locks')
        assert 'w1' in locks
        assert locks['w1'] == session.get('test_dict_locks', 'w1')