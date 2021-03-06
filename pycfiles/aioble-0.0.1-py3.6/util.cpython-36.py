# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aioble/corebluetooth/util.py
# Compiled at: 2019-06-13 01:58:06
# Size of source mod 2**32: 2416 bytes
import asyncio, functools, libdispatch

def dispatched_to_queue(method=None, wait=True):
    """Dispatches the method call to the object's dispatch queue

    This decorator functions assumes that the object has an attribute
    named '_queue' that contains the libdispatch.queue to dispatch the
    call to.

    Args:
        wait: If set to True the method call will be dispatched to the
            queue and but the asyncio thread will await the result
            returned from the block submitted to the dispatch queue.
            Defaults to true.

    Returns:
        The result of the method if wait is set to true. None will be
        be returned if wait is false.
    """

    def func(method):

        @functools.wraps(method)
        async def wrapper(self, *args, **kwargs):
            if wait:
                loop = asyncio.get_event_loop()
                future = loop.create_future()

                def queue_block():
                    result = method(self, *args, **kwargs)

                    def loop_block():
                        future.set_result(result)

                    loop.call_soon_threadsafe(loop_block)

                libdispatch.dispatch_async(self._queue, queue_block)
                return await future
            else:

                def queue_block():
                    method(self, *args, **kwargs)

                libdispatch.dispatch_async(self._queue, queue_block)
                return

        return wrapper

    return func


def dispatched_to_loop(method=None):
    """Asynchronously dispatches the method call to the asyncio event loop

    This decorator assumes that the object has an attribute named 'loop'
    that contains the event loop to dispatch the call to.

    Returns:
        None
    """

    def func(method):

        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            asyncio.run_coroutine_threadsafe((functools.partial)(method, self, *args, **kwargs)(), self.loop)

        return wrapper

    return func


class NSErrorException(Exception):

    def __init__(self, nserror):
        self.domain = nserror.domain()
        self.code = nserror.code()
        self.userInfo = nserror.userInfo()
        self.error = nserror

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"NSError(domain={self.domain}, code={self.code}, userInfo={self.userInfo})"