# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/heap/HeapManager.py
# Compiled at: 2020-01-30 06:21:49
# Size of source mod 2**32: 4602 bytes
""" Class description goes here. """
from weakref import WeakValueDictionary
import logging
from abc import ABCMeta, abstractmethod
import threading
from dataclay.util import Configuration
import six

@six.add_metaclass(ABCMeta)
class HeapManager(threading.Thread):
    __doc__ = "\n    @summary: This class is intended to manage all dataClay objects in runtime's memory.\n    "
    logger = None

    def __init__(self, theruntime):
        """
        @postcondition: Constructor of the object called from sub-class
        @param theruntime: Runtime being managed 
        """
        self.inmemory_objects = WeakValueDictionary()
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self.runtime = theruntime
        self.logger = logging.getLogger(__name__)
        self.daemon = True
        self.logger.debug('HEAP MANAGER created.')

    def get_heap(self):
        return self.inmemory_objects

    def shutdown(self):
        """Stop this thread"""
        self.logger.debug('HEAP MANAGER shutdown request received.')
        self._finished.set()

    def run(self):
        """
        @postcondition: Overrides run function 
        """
        gc_check_time_interval_seconds = Configuration.MEMMGMT_CHECK_TIME_INTERVAL / 1000.0
        while True:
            self.logger.trace('HEAP MANAGER THREAD is awake...')
            if self._finished.isSet():
                break
            self.run_task()
            self.logger.trace('HEAP MANAGER THREAD is going to sleep...')
            self._finished.wait(gc_check_time_interval_seconds)

        self.logger.debug('HEAP MANAGER THREAD Finished.')

    def _add_to_inmemory_map(self, dc_object):
        """
        @postcondition: the object is added to inmemory map
        @param dc_object: object to add
        """
        oid = dc_object.get_object_id()
        self.inmemory_objects[oid] = dc_object

    def update_object_id(self, old_object_id, new_object_id):
        """
        @postcondition: Updates heap references when an object changes id
        @param old_object_id: id of the old object id
        @param old_object_id: id of the new object id
        """
        try:
            self.inmemory_objects[new_object_id] = self.inmemory_objects.pop(old_object_id)
        except KeyError:
            self.logger.debug('Miss in Heap object %s' % str(old_object_id))

    def remove_from_heap(self, object_id):
        """
        @postcondition: Remove reference from Heap. Even if we remove it from the heap, 
        the object won't be Garbage collected till HeapManager flushes the object and releases it.
        @param object_id: id of object to remove from heap
        """
        self.inmemory_objects.pop(object_id)

    def get_from_heap(self, object_id):
        """
        @postcondition: Get from heap. 
        @param object_id: id of object to get from heap
        @return Object with id provided in heap or None if not found.
        """
        try:
            obj = self.inmemory_objects[object_id]
            self.logger.debug('Hit in Heap object %s' % str(object_id))
            return obj
        except KeyError:
            self.logger.debug('Miss in Heap object %s' % str(object_id))
            return

    def exists_in_heap(self, object_id):
        """
        @postcondition: Exists from heap. 
        @param object_id: id of object to get from heap
        @return True if exists. False otherwise.
        """
        try:
            if self.inmemory_objects[object_id] is None:
                return False
            return True
        except KeyError:
            return False

    def heap_size(self):
        """
        @postcondition: Get heap size. 
        @return Heap size
        """
        return len(self.inmemory_objects)

    @abstractmethod
    def flush_all(self):
        pass

    @abstractmethod
    def run_task(self):
        pass

    def cleanReferencesAndLockers(self):
        """
        @postcondition: Clean references and lockers not being used.
        """
        self.runtime.locker_pool.cleanLockers()