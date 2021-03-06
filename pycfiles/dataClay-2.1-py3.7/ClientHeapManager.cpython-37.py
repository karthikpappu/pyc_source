# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/heap/ClientHeapManager.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 1256 bytes
""" Class description goes here. """
import dataclay.heap.HeapManager as HeapManager
from threading import Timer

class ClientHeapManager(HeapManager):
    __doc__ = "\n    @summary: This class is intended to manage all dataClay objects in Client runtime's memory.\n    "

    def __init__(self, theruntime):
        """
        @postcondition: Constructor of the object 
        @param theruntime: Runtime being managed 
        """
        HeapManager.__init__(self, theruntime)
        self.logger.debug('CLIENT HEAP MANAGER created')

    def add_to_heap(self, dc_object):
        """
        @postcondition: the object is added to dataClay's heap
        @param dc_object: object to add to the heap 
        """
        HeapManager._add_to_inmemory_map(self, dc_object)

    def flush_all(self):
        """ 
        @postcondition: Does nothing. This function is intended to be used only in Execution Environment. Since 
        Heap Manager is an abstract class, we define this method as an "empty" method. Maybe I am missing some 
        better way to do that? (dgasull)
        """
        pass

    def run_task(self):
        self.cleanReferencesAndLockers()