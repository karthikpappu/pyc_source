# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xooof/xmldispatcher/servers/basic/xdhandlers.py
# Compiled at: 2008-10-01 10:39:53
import cPickle, time, logging
logging = logging.getLogger('xooof.xmldispatcher.servers.basic')
from xdserver import RequestHandlerBase, XMLDispatcherContext
from xooof.xmldispatcher.interfaces.interfaces import *
from xooof.xmldispatcher.tools.envelope.constants import *

class NullHandler(RequestHandlerBase):
    """A request handler that echoes the request.

    This one is typically used to test the communications layer."""
    __module__ = __name__

    def __init__(self):
        pass

    def process(self, request):
        request.xmlRply = request.xmlRqst
        request.sessionData = request.sessionData


class XMLDispatcherDelegatorHandler(RequestHandlerBase):
    """A request handler that delegates the request to an IXMLDispatcher"""
    __module__ = __name__

    def __init__(self, xd):
        self.__xd = xd

    def process(self, request):
        if request.verb == XD_VERB_CLASS_METHOD:
            (request.xmlRply, request.sessionData) = self.__xd.dispatchClassMethodXML(request.className, request.methodName, request.xmlRqst, request.sessionData)
        elif request.verb == XD_VERB_INSTANCE_METHOD:
            (request.xmlRply, request.sessionData) = self.__xd.dispatchInstanceMethodXML(request.className, request.methodName, request.instanceId, request.xmlRqst, request.sessionData)
        elif request.verb == XD_VERB_NEW_INSTANCE_METHOD:
            (request.xmlRply, request.sessionData) = self.__xd.dispatchNewInstanceMethodXML(request.className, request.methodName, request.xmlRqst, request.sessionData)
        else:
            raise XMLDispatcherAppException('Unexpected verb: ' + request.verb)


class RoleCheckerHandler(RequestHandlerBase):
    """A request handler for role-based security

    roleDefs must implement IRoleDefs
    roleChecker must implement IRoleChecker

    Expected from previous handler: request.xdCtx must be set.
    """
    __module__ = __name__

    def __init__(self, roleDefs, roleChecker, nextHandler):
        RequestHandlerBase.__init__(self, nextHandler)
        self.__roleDefs = roleDefs
        self.__roleChecker = roleChecker

    def process(self, request):
        if request.verb == XD_VERB_CLASS_METHOD:
            state = None
        elif request.verb == XD_VERB_INSTANCE_METHOD:
            instance = request.xdCtx.getInstance(request.className, request.instanceId)
            if hasattr(instance, 'getState'):
                state = instance.getState() or 'nihil'
            else:
                state = None
        elif request.verb == XD_VERB_NEW_INSTANCE_METHOD:
            state = 'nihil'
        else:
            raise XMLDispatcherAppException('Unexpected verb: ' + request.verb)
        if not self.__roleDefs.isAllowedByRole(request.xdCtx, self.__roleChecker, request.className, request.methodName, state):
            raise XMLDispatcherUserException('Access denied by XMLDispatcher role-based security', code='XDE_RBS_ACCESS_DENIED')
        self.processNext(request)
        return


class SimpleLoggerHandler(RequestHandlerBase):
    """A request handler that logs requests and replies"""
    __module__ = __name__

    def __init__(self, logger, nextHandler):
        RequestHandlerBase.__init__(self, nextHandler)
        self.__logger = logger

    def process(self, request):
        if request.verb == XD_VERB_CLASS_METHOD:
            instanceInfo = ''
        elif request.verb == XD_VERB_INSTANCE_METHOD:
            instanceInfo = '[%s]' % (request.instanceId,)
        elif request.verb == XD_VERB_NEW_INSTANCE_METHOD:
            instanceInfo = '[]'
        else:
            raise XMLDispatcherAppException('Unexpected verb: ' + request.verb)
        callString = '%s%s::%s' % (request.className, instanceInfo, request.methodName)
        self.__logger.info('%s starting' % callString)
        self.__logger.debug('RQST: ' + request.xmlRqst)
        try:
            self.processNext(request)
        except XMLDispatcherUserException:
            self.__logger.error('%s failed' % callString, exc_info=1)
            raise
        except:
            self.__logger.critical('%s failed' % callString, exc_info=1)
            raise
        else:
            self.__logger.debug('RPLY: ' + request.xmlRply)
            self.__logger.info('%s succeeded' % callString)


class MarshallerHandler(RequestHandlerBase):
    """A request handler that unmarshalls xmlRqst and marshalls xmlRply.

    Expected from next handler: request.rply must be final
    """
    __module__ = __name__

    def __init__(self, marshaller, nextHandler):
        """Constructor.

        marshaller must implement xooof.xmldispatcher.tools.marshaller.IXMLDispatcherMarshaller.IXMLDispatcherMarshaller
        """
        RequestHandlerBase.__init__(self, nextHandler)
        self.__marshaller = marshaller

    def process(self, request):
        request.rqst = self.__marshaller.unmarshall(request.xmlRqst)
        self.processNext(request)
        if request.verb == XD_VERB_NEW_INSTANCE_METHOD:
            request.xmlRply = self.__marshaller.marshallId(request.rply)
        else:
            request.xmlRply = self.__marshaller.marshall(request.rply)


class SessionHandler(RequestHandlerBase):
    """A request handler that unpacks sessionData and packs session.

    It also handles session expiration.

    Expected from next handler: request.session must be final
    """
    __module__ = __name__

    def __init__(self, ttl, nextHandler):
        RequestHandlerBase.__init__(self, nextHandler)
        self.__ttl = ttl

    def unmarshalSessionData(self, sessionData):
        if sessionData:
            (exp, session) = cPickle.loads(sessionData)
            if exp < time.clock():
                raise XMLDispatcherUserException('Session expired', code='XDE_SES_EXPIRED')
        else:
            session = None
        return session

    def marshalSession(self, session):
        if session:
            sessionData = cPickle.dumps((time.clock() + self.__ttl, session))
        else:
            sessionData = None
        return sessionData

    def process(self, request):
        request.session = self.unmarshalSessionData(request.sessionData)
        self.processNext(request)
        request.sessionData = self.marshalSession(request.session)


class DefaultXdCtxHandler(RequestHandlerBase):
    """A request handler that sets up the xdCtx field of the request"""
    __module__ = __name__

    def __init__(self, nextHandler):
        RequestHandlerBase.__init__(self, nextHandler)

    def makeXMLDispatcherContext(self, request):
        return XMLDispatcherContext()

    def process(self, request):
        request.xdCtx = self.makeXMLDispatcherContext(request)
        try:
            if hasattr(request, 'session'):
                request.xdCtx.setSession(request.session)
            self.processNext(request)
            if hasattr(request, 'session'):
                request.session = request.xdCtx.getSession()
        finally:
            request.xdCtx = None
        return


class XdCtxCacheHandler(RequestHandlerBase):
    """A request handler that flushes the xdCtx cache.

    Expected from previous handler: request.xdCtx must be set.
    """
    __module__ = __name__

    def __init__(self, nextHandler):
        RequestHandlerBase.__init__(self, nextHandler)

    def _flushCacheNoRaise(self, request):
        try:
            request.xdCtx.flushCache(willRollback=1)
        except:
            logging.warn('Exception while flushing cache', exc_info=1)

    def process(self, request):
        try:
            self.processNext(request)
        except:
            self._flushCacheNoRaise(request)
            raise
        else:
            request.xdCtx.flushCache()


class ImplicitContextRegistrationHandler(RequestHandlerBase):
    """A request handler that registers the context in a global context manager (see ctxmgr module)."""
    __module__ = __name__

    def __init__(self, xdCtxMgr, nextHandler):
        RequestHandlerBase.__init__(self, nextHandler)
        self.__xdCtxMgr = xdCtxMgr

    def process(self, request):
        self.__xdCtxMgr.registerContextForThread(request.xdCtx)
        try:
            self.processNext(request)
        finally:
            self.__xdCtxMgr.unregisterContextForThread()


class ImplicitContextInvokerHandler(RequestHandlerBase):
    """A request handler that invokes the business method and stores request.rply.

    This request handler does not pass the XMLDispatcherContext explicitly
    to methods, assuming it has been registered globally in a threaded
    context manager (see ctxmgr module).

    Expected from previous handler: request.xdCtx must be set.
    """
    __module__ = __name__

    def __init__(self):
        RequestHandlerBase.__init__(self, None)
        return

    def _checkMethod(self, o, className, methodName, verb):
        if verb == XD_VERB_CLASS_METHOD:
            methodNames = o._public_class_methods
            category = 'class method'
        elif verb == XD_VERB_NEW_INSTANCE_METHOD:
            methodNames = o._public_constructors
            category = 'constructor'
        elif verb == XD_VERB_INSTANCE_METHOD:
            methodNames = o._public_instance_methods
            category = 'instance method'
        else:
            raise XMLDispatcherAppException('Unexpected verb: ' + verb)
        if methodName not in methodNames:
            raise XMLDispatcherUserException('%s is not a public %s of class %s' % (methodName, category, className), code='XDE_DSP_NOT_A_METHOD')

    def _getMethod(self, o, className, methodName):
        try:
            return getattr(o, methodName)
        except:
            logging.error('Could not get method %s', exc_info=1)
            raise XMLDispatcherUserException('Invalid method name %s for class %s(see server log for details)' % (methodName, className), code='XDE_DSP_NOT_A_METHOD')

    def process(self, request):
        args = (
         request.rqst,)
        if request.verb == XD_VERB_CLASS_METHOD:
            klass = request.xdCtx.getClass(request.className)
            self._checkMethod(klass, request.className, request.methodName, request.verb)
            request.rply = apply(self._getMethod(klass, request.className, request.methodName), args)
        elif request.verb == XD_VERB_INSTANCE_METHOD:
            instance = request.xdCtx.getInstance(request.className, request.instanceId)
            self._checkMethod(instance, request.className, request.methodName, request.verb)
            request.rply = apply(self._getMethod(instance, request.className, request.methodName), args)
        elif request.verb == XD_VERB_NEW_INSTANCE_METHOD:
            klass = request.xdCtx.getClass(request.className)
            self._checkMethod(klass, request.className, request.methodName, request.verb)
            r = apply(self._getMethod(klass, request.className, request.methodName), args)
            if isinstance(r, klass):
                instance = r
                instanceId = instance.getInstanceId()
                assert instance is request.xdCtx.getInstance(request.className, instanceId)
            else:
                instanceId = r
                instance = request.xdCtx._getNewInstance(request.className, instanceId)
                apply(self._getMethod(instance, request.className, 'post' + request.methodName[0].upper() + request.methodName[1:]), args)
                assert instanceId == instance.getInstanceId()
            request.rply = instanceId
        else:
            raise XMLDispatcherAppException('Unexpected verb: ' + request.verb)