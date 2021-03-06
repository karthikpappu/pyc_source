# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/abstract/callback.py
# Compiled at: 2020-05-13 19:27:59
# Size of source mod 2**32: 21250 bytes
from __future__ import print_function, division, absolute_import
import logging
from traceback import format_exc
from tpDcc.libs.python import decorators
LOGGER = logging.getLogger()

class ICallback(object):
    __doc__ = '\n    Class that defines basic callback interface functions\n    '

    @classmethod
    @decorators.abstractmethod
    def register(cls, fn, owner=None):
        """
        Register the given Python function
        :param fn: function, python function to register
        :param owner: class, class owner of the function
        :return: token of non defined type to later unregister the function
        """
        pass

    @classmethod
    @decorators.abstractmethod
    def unregister(cls, token):
        """
        Unregister the given Python function
        :param token: token, token provided by register method
        """
        pass

    @classmethod
    @decorators.abstractmethod
    def filter(cls, *args):
        """
        Function used to process the arguments during an execution of a callback
        :param args: variable list of arguments pass from the callback function to be evaluated
        """
        return (False, None)


class AbstractCallback(object):
    __doc__ = '\n    Class that defines basic callback interface functions\n    This class manages a pair of notifier and listener objects\n    '

    def __init__(self, notifier, shutdown_notifier, owner=None):
        super(AbstractCallback, self).__init__()
        self._notifier = notifier
        self._enabled_stack = list()
        self._registry = list()
        self._shutdown_notifier = None
        self._shutdown_token = None
        if shutdown_notifier:
            if notifier != shutdown_notifier:
                self._shutdown_notifier = shutdown_notifier
                self._shutdown_token = self._shutdown_notifier.register(self._shutdown)

    def __del__(self):
        if self._notifier:
            self._shutdown([])

    def _connect(self, fn):
        """
        Internal callback registration function
        :param fn: Python function to register as a listener to the Sender
        :return:
        """
        return self._notifier.register(fn)

    def _disconnect(self, token):
        """
        Internal callback unregistration function
        :param token: valid token returned from a previuous _connect() call
        :return: None if unregistration was successfull or the unchanged value from token otherwise
        """
        if token:
            return self._notifier.unregister(token)

    def _filter(self, *args):
        """
        Internal function to evaluate if the callback from the notifier is valid.
            Test the validity of the message with the custom function.
        @param *args A variable list of arguments receivied from the notifier.
        @return      A tuple of indeterminant length (bool, object, ...) that is (True, Valid Data, ...) if callback
            should be passed to the listners; (False, None) otherwise.
        """
        return (self._notifier.filter)(*args)

    def _shutdown(self, *args):
        """
        Forces an unregistering and disconnection from the sender. This method should be overriden by subclasse
        """
        if self._shutdown_token:
            if self._shutdown_notifier:
                self._shutdown_notifier.unregister(self._shutdown_token)
        self._shutdown_notifier = None
        self._notifier = None

    def _push(self, state):
        """
        Function to set the enable state while maintaining a history of previous enabled states
        :param state: bool, the enable state of the callback
        """
        if self.valid:
            self._enabled_stack.append(self.enabled)
            self.enabled = state

    def _pop(self):
        """
        Function to restore the enable state to a previous enabled state
        :return: True if the callback is enabled as a result of the restoration or False otherwise
        """
        if self.valid:
            if self._enabled_stack:
                self.enabled = self._enabled_stack.pop()
        return self.enabled

    @property
    def valid(self):
        """!
        Convenience property to query the validity of this callback.
        @return True if the callback has a notifier; False otherwise.
        """
        return bool(self._notifier)

    @property
    def empty(self):
        """
        Convenience property to query the existence of listeners to this callback.
        @return True if the callback has listeners registered; False otherwise.
        @warning This method must be overriden by subclasses.
        """
        return True

    @property
    def connected(self):
        """
        Convenience property to query the 'connected' state of the callback.
        @return True if the callback has connected itself with the INotifier implementation.
        @warning This method must be overriden by subclasses.
        """
        return False

    @property
    def enabled(self):
        """
        Convenience property to query the 'not empty' and 'connected' state of the callback.
        @return True if the callback has listeners and is connected the to the INotifier implementation.
        @warning This method must be overriden by subclasses.
        """
        return False

    @property
    def registry(self):
        """
        Convenience property to query all registerd functions of a callback
        :return: list<fn>
        """
        pass

    @enabled.setter
    def enabled(self, value):
        """
        Convenience property to set the 'enable' state of the callback.  Modifying the enable state either toggles
            the 'connected' state of the callback but maintains the list of listeners.
        @param value The enable state of the callback.
        @warning This method must be overriden by subclasses.
        """
        pass

    def suspend(self):
        """
        Method to the suspend the callback connection.
        """
        self._push(False)

    def resume(self):
        """
        Method to resume the nofitication connection.
        @return True if the callback connection has been resumed succesfully; False otherwise.
        """
        return self._pop()

    def unregister(self, fn):
        """
        Removes a listener from this inestance.
        @param fn A valid python function with a variable number of arguments (i.e. *args).
        @warning This method must be overriden by subclasses.
        """
        pass

    def register(self, fn, owner=None):
        """
        Adds a listener to this instance.

        @param fn A valid python function with a variable number of arguments (i.e. *args).
        @param owner: class, owner of the callback
        @warning This method must be overriden by subclasses.
        """
        pass

    def unregister_owner_callbacks(self, owner):
        """
        Removes all notifiers registered by a certain owner
        :param owner: class
        """
        pass

    def cleanup(self):
        """
        Method to terminate the callback
        """
        return self._shutdown()


class SimpleCallback(AbstractCallback):
    __doc__ = '\n    Simple implementation of Abstractcallback interface\n    It maintains a one-to-one relationship between listener and notifiers whitout any event filtering\n    '

    class RegistryEntry(object):

        def __init__(self, callback, token, owner=None):
            self.callback = callback
            self.token = token
            self.owner = owner

    def __init__(self, notifier, shutdown_notifier, owner=None):
        super(SimpleCallback, self).__init__(notifier=notifier, shutdown_notifier=shutdown_notifier, owner=owner)

    def _shutdown(self, *args):
        LOGGER.debug('Started: ({}) {} Shutdown'.format(str(self._notifier), self.__class__.__name__))
        for entry in self._registry:
            LOGGER.debug('{}._shutdown - Disconnecting ({})'.format(str(self._notifier), self.__class__.__name__, str(entry)))
            entry.token = self._disconnect(entry.token)

        del self._registry[:]
        (super(self.__class__, self)._shutdown)(*args)
        LOGGER.debug('Complete: ({}) {} Shutdown'.format(str(self._notifier), self.__class__.__name__))

    @property
    def empty(self):
        """
        Convenience property to query the existence of listeners to this callback.
        @return True if the callback has listeners registered; False otherwise.
        """
        return not bool(self._registry)

    @property
    def connected(self):
        """
        Convenience property to query the 'connected' state of the callback.
        @return True if the callback has connected itself with the INotifier implementation.
        """
        return all(e.token for e in self._registry)

    @property
    def enabled(self):
        """
        Convenience property to query the 'not empty' and 'connected' state of the callback.
        @return True if the callback has listeners and is connected the to the INotifier implementation.
        """
        return not self.empty and bool(self.connected)

    def invoke_callbacks(self):
        """
        Manually invoke all the callbacks registered to the callback
        """
        for entry in self._registry:
            try:
                entry.callback()
            except Exception:
                from traceback import format_exc
                LOGGER.error(format_exc())

    @enabled.setter
    def enabled(self, value):
        """!
        Convenience property to set the 'enable' state of the callback.  Modifying the enable state either toggles
            the 'connected' state of the callback but maintains the list of listeners.

        @param value The enable state of the callback.
        """
        for entry in self._registry:
            if not value and entry.token:
                entry.token = self._disconnect(entry.token)
            else:
                if value and not entry.token:
                    entry.token = self._connect(entry.callback)

    def register(self, fn, owner=None):
        """
        Adds a listener to this instance
        @param fn: a valid Python function with a varaible number of arguments (exp. *args)
        @param owner: class, owner of the callback
        """
        entry = next((e for e in self._registry if e.callback == fn), None)
        LOGGER.debug('Started: ({}) {} Register - fn:"{}", owner:"{}", entry:"{}"'.format(str(self._notifier), self.__class__.__name__, str(fn), owner, str(entry)))
        if not entry:
            token = self._connect(fn) if self.connected else None
            LOGGER.debug('({}) {} Register - token:"{}"'.format(str(self._notifier), self.__class__.__name__, str(token)))
            self._registry.append(SimpleCallback.RegistryEntry(fn, token, owner=owner))
        LOGGER.debug('Completed: ({}) {} Register'.format(str(self._notifier), self.__class__.__name__))

    def unregister(self, fn):
        """
        Removes a listener from this instance
        :param fn: a valid Python function with a varaible number of arguments (exp. *args)
        """
        entry = next((e for e in self._registry if e.callback == fn), None)
        LOGGER.debug('Started: ({}) {} Unregister - fn:"{}", entry:"{}"'.format(str(self._notifier), self.__class__.__name__, str(fn), str(entry)))
        if entry:
            self._disconnect(entry.token)
            self._registry.remove(entry)
        LOGGER.debug('Completed: ({}) {} Unregister'.format(str(self._notifier), self.__class__.__name__))

    def unregister_owner_callbacks(self, owner):
        """
        Removes all notifiers registered by a certain owner
        :param owner: class
        """
        entry = next((e for e in self._registry if e.owner == owner), None)
        LOGGER.debug('Started: ({}) {} Unregister - owner:"{}", entry:"{}"'.format(str(self._notifier), self.__class__.__name__, str(owner), str(entry)))
        if entry:
            self._disconnect(entry.token)
            self._registry.remove(entry)
        LOGGER.debug('Completed: ({}) {} Unregister'.format(str(self._notifier), self.__class__.__name__))


class FilterCallback(AbstractCallback, object):
    __doc__ = '\n    Provides a implementatino of an Abstractcallback interface that allows the filtering of the callback\n    generated from the notifier. It maintains a many-to-one relationship between listeners and notifier\n    '

    class RegistryEntry(object):

        def __init__(self, callback, owner=None):
            self.callback = callback
            self.owner = owner

    def __init__(self, notifier, shutdown_notifier, owner=None):
        super(FilterCallback, self).__init__(notifier=notifier, shutdown_notifier=shutdown_notifier, owner=owner)
        self._token = None

    def _shutdown(self, *args):
        LOGGER.debug('Started: ({}) {} Shutdown'.format(str(self._notifier), self.__class__.__name__))
        if self._token:
            self._token = self._disconnect(self._token)
            self._token = None
        del self._registry[:]
        (super(self.__class__, self)._shutdown)(*args)
        LOGGER.debug('Complete: ({}) {} Shutdown'.format(str(self._notifier), self.__class__.__name__))

    def _notify(self, *args):
        """
        Internal function registered with the notifier. Evaluates the condition with _filter during the callback.
        If its valid, it will broadcast the callback to the listener via _execute().
        All notifier data is passed on to the user via _execute().
        :param args: A variable list of arguments received from the notifier
        :return:
        """
        fargs = (self._filter)(*args)
        if fargs[0]:
            (self._execute)(*fargs[1:])

    def _execute(self, *args):
        """
        Internal function to notify all listeners registered to the current instance of the class
        :param args: A variable list of arguments received from the notifier
        """
        for entry in self._registry:
            try:
                (entry.callback)(*args)
            except Exception:
                LOGGER.error(format_exc())

    @property
    def empty(self):
        """
        Convenience property to query the existence of listeners to this callback.
        @return True if the callback has listeners registered; False otherwise.
        """
        return not bool(self._registry)

    @property
    def connected(self):
        """
        Convenience property to query the 'connected' state of the callback.
        @return True if the callback has connected itself with the INotifier implementation.
        """
        return bool(self._token)

    @property
    def enabled(self):
        """
        Convenience property to query the 'not empty' and 'connected' state of the callback.
        @return True if the callback has listeners and is connected the to the INotifier implementation.
        """
        return not self.empty and bool(self.connected)

    @enabled.setter
    def enabled(self, value):
        """!
        Convenience property to set the 'enable' state of the callback.  Modifying the enable state either toggles
            the 'connected' state of the callback but maintains the list of listeners.

        @param value The enable state of the callback.
        """
        if not value:
            if self._token:
                self._token = self._disconnect(self._token)
        if value:
            if not self._token:
                self._token = self._connect(self._notify)

    def register(self, fn, owner=None):
        """
        Adds a listener to this instance
        @param fn: a valid Python function with a variable number of arguments (exp. *args)
        @param owner: class, owner of the callback
        """
        LOGGER.debug('Started: ({}) {} Register - fn:"{}", owner:"{}", IsEmpty:"{}"'.format(str(self._notifier), self.__class__.__name__, str(fn), owner, bool(self.empty)))
        if self.empty:
            self._token = self._connect(self._notify)
            LOGGER.debug('({}) {} Register - token:"{}"'.format(str(self._notifier), self.__class__.__name__, str(self._token)))
        self._registry.append(FilterCallback.RegistryEntry(fn, owner=owner))
        LOGGER.debug('Completed: ({}) {} Register'.format(str(self._notifier), self.__class__.__name__))

    def unregister(self, fn):
        """
        Removes a listener from this instance
        :param fn: a valid Python function with a varaible number of arguments (exp. *args)
        """
        entry = next((e for e in self._registry if e.callback == fn), None)
        LOGGER.debug('Started: ({}) {} Unregister - fn:"{}", IsEmpty:"{}"'.format(str(self._notifier), self.__class__.__name__, str(fn), bool(self.empty)))
        if entry:
            self._registry.remove(entry)
        if self.empty:
            if self.connected:
                LOGGER.debug('({}) {} Unregister token:"{}"'.format(str(self._notifier), self.__class__.__name__, str(self._token)))
                self._token = self._disconnect(self._token)
        LOGGER.debug('Completed: ({}) {} Unregister'.format(str(self._notifier), self.__class__.__name__))

    def unregister_owner_callbacks(self, owner):
        """
        Removes all notifiers registered by a certain owner
        :param owner: class
        """
        entry = next((e for e in self._registry if e.owner == owner), None)
        LOGGER.debug('Started: ({}) {} Unregister - owner:"{}", entry:"{}"'.format(str(self._notifier), self.__class__.__name__, str(owner), str(entry)))
        if entry:
            self._registry.remove(entry)
        if self.empty:
            if self.connected:
                LOGGER.debug('({}) {} Unregister token:"{}"'.format(str(self._notifier), self.__class__.__name__, str(self._token)))
                self._token = self._disconnect(self._token)
        LOGGER.debug('Completed: ({}) {} Unregister'.format(str(self._notifier), self.__class__.__name__))


class CallbackInstance(object):
    __doc__ = '\n    Utility class to sync callback registration to the lifetime of an object instance\n    '

    def __init__(self, callback, fn):
        super(CallbackInstance, self).__init__()
        self._notify = fn
        self._callback = callback
        if self._callback:
            self._callback.register(self._notify)

    def __del__(self):
        """
        Destructor
        """
        if self._callback:
            self._callback.unregister(self._notify)
        self._callback = None
        self._notify = None

    @property
    def callback(self):
        """
        Convenience property to access the callback implementation associated with this callbackInstance
        """
        return self._callback


class PythonTickCallback(ICallback, object):
    __doc__ = '\n    This notifier implements a Tick notifier\n    '
    interval = 0.05
    tick_threads = dict()

    @classmethod
    def register(cls, fn):
        """
        Register the given Python function
        :param fn: function, python function to register
        :return: token of non defined type to later unregister the function
        """
        fn_id = id(fn)
        if cls.tick_threads.get(fn_id, None) is not None:
            LOGGER.warning('{} already registered with PythonTickNotifier'.format(str(fn)))
            return
        else:
            repeater = cls._tick(fn_id)
            cls.tick_threads[fn_id] = (fn, repeater)
            return fn_id

    @classmethod
    def unregister(cls, token):
        """
        Unregister the given Python function
        :param token: token, token provided by register method
        """
        pair = cls.tick_threads.get(token, None)
        if pair:
            pair[1].stop()
            del cls.tick_threads[token]

    @classmethod
    @decorators.repeater(interval)
    def _tick(cls, token):
        """
        Internal function to handl the tick event
        :param token: token, token provided by register function
        """
        pair = cls.tick_threads.get(token, None)
        if pair:
            pair[0]()