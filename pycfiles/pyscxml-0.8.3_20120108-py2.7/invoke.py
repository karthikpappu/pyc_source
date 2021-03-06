# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/scxml/invoke.py
# Compiled at: 2012-01-08 09:10:03
""" 
This file is part of pyscxml.

    pyscxml is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyscxml is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with pyscxml.  If not, see <http://www.gnu.org/licenses/>.
    
    
    @author Johan Roxendal
    @contact: johan@roxendal.com
"""
from louie import dispatcher
from messaging import exec_async
from functools import partial
from scxml.messaging import UrlGetter
import logging, eventlet

class InvokeWrapper(object):

    def __init__(self):
        self.logger = logging.getLogger('pyscxml.invoke.%s' % type(self).__name__)
        self.invoke = lambda : None
        self.invokeid = None
        self.cancel = lambda : None
        self.invoke_obj = None
        self.autoforward = False
        return

    def set_invoke(self, inv):
        inv.logger = self.logger
        self.invoke_obj = inv
        self.invokeid = inv.invokeid
        inv.autoforward = self.autoforward
        self.cancel = inv.cancel
        self.send = getattr(inv, 'send', None)
        return

    def finalize(self):
        if self.invoke_obj:
            self.invoke_obj.finalize()


class BaseInvoke(object):

    def __init__(self):
        self.invokeid = None
        self.parentSessionid = None
        self.autoforward = False
        self.src = None
        self.finalize = lambda : None
        return

    def start(self, parentQueue):
        pass

    def cancel(self):
        pass

    def __str__(self):
        return '<Invoke id="%s">' % self.invokeid


class BaseFetchingInvoke(BaseInvoke):

    def __init__(self):
        BaseInvoke.__init__(self)
        self.getter = UrlGetter()
        dispatcher.connect(self.onHttpResult, UrlGetter.HTTP_RESULT, self.getter)
        dispatcher.connect(self.onFetchError, UrlGetter.HTTP_ERROR, self.getter)
        dispatcher.connect(self.onFetchError, UrlGetter.URL_ERROR, self.getter)

    def onFetchError(self, signal, exception, **named):
        self.logger.error(str(exception))
        dispatcher.send('error.communication.invoke.' + self.invokeid, self, data=exception)

    def onHttpResult(self, signal, result, **named):
        self.logger.debug('onHttpResult ' + str(named))
        dispatcher.send('result.invoke.%s' % self.invokeid, self, data=result)


class InvokeSCXML(BaseFetchingInvoke):

    def __init__(self, data):
        BaseFetchingInvoke.__init__(self)
        self.sm = None
        self.parentQueue = None
        self.content = None
        self.initData = data
        self.cancelled = False
        self.default_datamodel = 'python'
        return

    def start(self, parentQueue):
        self.parentQueue = parentQueue
        if self.src:
            self.getter.get_async(self.src, None)
        else:
            self._start(self.content)
        return

    def _start(self, doc):
        if self.cancelled:
            return
        from pyscxml import StateMachine
        self.sm = StateMachine(doc, sessionid=self.parentSessionid + '.' + self.invokeid, default_datamodel=self.default_datamodel, log_function=lambda label, val: dispatcher.send(signal='invoke_log', sender=self, label=label, val=val))
        self.interpreter = self.sm.interpreter
        self.sm.compiler.initData = self.initData
        dispatcher.send('created', sender=self, sm=self.sm)
        self.sm._start_invoke(self.parentQueue, self.invokeid)
        eventlet.spawn(self.sm.interpreter.mainEventLoop)

    def send(self, eventobj):
        if self.sm and not self.sm.isFinished():
            self.sm.interpreter.externalQueue.put(eventobj)

    def onHttpResult(self, signal, result, **named):
        self.logger.debug('onHttpResult ' + str(named))
        self._start(result)

    def cancel(self):
        self.cancelled = True
        if not self.sm:
            return
        self.sm.interpreter.running = False

        class DummyQueue(object):

            def put(self, item):
                pass

        self.sm.datamodel['_parent'] = DummyQueue()
        self.sm._send(['cancel', 'invoke', self.invokeid], {}, self.invokeid)


class InvokeHTTP(BaseFetchingInvoke):

    def __init__(self):
        BaseFetchingInvoke.__init__(self)

    def send(self, eventobj):
        self.getter.get_async(self.content, eventobj.data, type=eventobj.name.join('.'))

    def start(self, parentQueue):
        dispatcher.send('init.invoke.' + self.invokeid, self)

    def onHttpResult(self, signal, result, **named):
        self.logger.debug('onHttpResult ' + str(named))
        dispatcher.send('result.invoke.%s' % self.invokeid, self, data={'response': result})


class InvokeSOAP(BaseInvoke):

    def __init__(self):
        BaseInvoke.__init__(self)
        self.client = None
        return

    def start(self, parentQueue):
        exec_async(self.init)

    def init(self):
        from suds.client import Client
        self.client = Client(self.content)
        dispatcher.send('init.invoke.' + self.invokeid, self)

    def send(self, eventobj):
        exec_async(partial(self.soap_send_sync, ('.').join(eventobj.name), eventobj.data))

    def soap_send_sync(self, method, data):
        result = getattr(self.client.service, method)(**data)
        dispatcher.send('result.invoke.%s.%s' % (self.invokeid, method), self, data=result)


__all__ = [
 'InvokeWrapper', 'InvokeSCXML', 'InvokeSOAP', 'InvokeHTTP']