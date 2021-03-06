# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/minitestlib/TestObject.py
# Compiled at: 2009-01-22 06:07:01
"""
TestObject is a basic class for all objects in journal file
"""
__author__ = 'Andy Shevchenko <andy.shevchenko@gmail.com>'
__revision__ = '$Id$'
__all__ = [
 'TestObject',
 'diff',
 'diff_keys_by_result',
 'get_keys_by_result',
 'get_objects_by_result']
import copy
from minitestlib.Log import logger
from minitestlib.OrderedDict import OrderedDict

class TestObject:
    """ Basement for each journal object """

    def __init__(self, parent, key):
        self.parent = parent
        self.key = key
        self.lines = []
        self.objects = OrderedDict()
        self.results = {}
        self.amount = 0
        self.collected = False
        self.name = 'noname'

    def dbg(self, msg):
        """ Internal debbuging """
        logger.debug('%s: %s' % (self.__class__.__name__, msg))

    def append(self, line):
        """ Append line to object """
        self.lines.append(line)

    def __len__(self):
        """ Represent length of object as length of its container """
        return len(self.objects)

    def __getitem__(self, key, result=None):
        """ Get item from container by key """
        return self.objects.get(key, result)

    def keys(self):
        """ Get container's keys """
        return self.objects.keys()

    def get_keys(self):
        """ Get keys as a list of parent's keylist and self key """
        if self.parent is None:
            return [
             self.key]
        keys = self.parent.get_keys()
        keys.append(self.key)
        return keys

    def get_results(self):
        """ Return collected results """
        return self.results

    def get_amount(self):
        """ Return overall amount of collected results """
        return self.amount

    def summarize(self):
        """ Summarize results of childs """
        if self.collected or len(self.objects) == 0:
            return
        for obj_key in self.objects.keys():
            self.objects[obj_key].summarize()
            results = self.objects[obj_key].get_results()
            for result_key in results.keys():
                if self.results.has_key(result_key):
                    self.results[result_key] += results[result_key]
                else:
                    self.results[result_key] = results[result_key]

            self.amount += self.objects[obj_key].get_amount()

        self.collected = True


def diff(old, new, removed, added, changed):
    """ Get difference between two objects """
    if len(old) == 0 and len(new) == 0:
        results_old = old.get_results()
        results_new = new.get_results()
        results_set = set(results_old.keys() + results_new.keys())
        if len(results_set) == 0:
            return
        if len(results_set) == 1:
            if len(results_old) == 1 and len(results_new) == 1:
                return
        changed.append([old, new])
    else:
        keys_old = old.keys()
        keys_new = new.keys()
        for key in set(keys_old + keys_new):
            if key not in keys_new:
                removed.append(old[key])
            elif key not in keys_old:
                added.append(new[key])
            else:
                diff(old[key], new[key], removed, added, changed)


def diff_keys_by_result(old, new, start_depth=0):
    """ Get difference between objects key traces """
    old_keys = get_keys_by_result(old, start_depth)
    new_keys = get_keys_by_result(new, start_depth)
    for name in old_keys.keys():
        if name not in new_keys.keys():
            continue
        keys_copy = copy.copy(old_keys[name])
        for keys in keys_copy:
            if keys in new_keys[name]:
                old_keys[name].remove(keys)
                new_keys[name].remove(keys)

        if len(old_keys[name]) == 0:
            del old_keys[name]
        if len(new_keys[name]) == 0:
            del new_keys[name]

    return (
     old_keys, new_keys)


def get_keys_by_result(starter, start_depth=0):
    """ Fill structure by key traces of given objects """
    objects = {}
    get_objects_by_result(starter, objects)
    keys = {}
    for name in objects.keys():
        keys[name] = []
        for obj in objects[name]:
            keys[name].append(obj.get_keys()[start_depth:])

    return keys


def get_objects_by_result(starter, objects):
    """ Collect objects in the dependency of their result recursively """
    if len(starter) == 0:
        for result in starter.get_results():
            if result not in objects.keys():
                objects[result] = []
            objects[result].append(starter)

    for key in starter.keys():
        get_objects_by_result(starter[key], objects)