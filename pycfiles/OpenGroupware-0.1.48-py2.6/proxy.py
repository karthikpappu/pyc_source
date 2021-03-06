# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/proxy/proxy.py
# Compiled at: 2012-10-12 07:02:39
import xmlrpclib, transport, time
from base64 import b64decode
from coils.net import *
from coils.foundation import fix_microsoft_text
from coils.core.omphalos import associate_omphalos_representation, disassociate_omphalos_representation

class Proxy(Protocol, PathObject):
    __pattern__ = 'proxy'
    __namespace__ = None
    __xmlrpc__ = False
    __ResultTranscode__ = None

    def __init__(self, parent, **params):
        self.name = 'proxy'
        PathObject.__init__(self, parent, **params)
        if Proxy.__ResultTranscode__ is None:
            sd = ServerDefaultsManager()
            Service.__PayloadTranscode__ = sd.bool_for_default('CoilsXMLRPCProxyTranscode')
            self.log.debug('XML-RPC Proxy Transcoded Results Enabled')
            Service.__ProxyHost__ = sd.string_for_default('CoilsXMLRPCProxyTarget', value='127.0.0.1')
            self.log.debug(('XML-RPC Proxy Target is "{0}"').format(Service.__ProxyHost__))
        return

    def local_methods(self):
        return [
         'zogi.getLoginAccount', 'zogi.getTombstone']

    def do_POST(self):
        request = self.request
        authorization = request.headers.get('authorization')
        if authorization == None:
            raise AuthenticationException('Authentication Required')
        (kind, data) = authorization.split(' ')
        if kind == 'Basic':
            (username, _, password) = b64decode(data).partition(':')
        else:
            raise 'Proxy can only process Basic authentication'
            return
        payload = request.get_request_payload()
        if Service.__PayloadTranscode__:
            self.log.debug('XML-RPC Proxy Transcoding Results')
            payload = fix_microsoft_text(payload)
        rpc = xmlrpclib.loads(payload, use_datetime=True)
        x = transport.Transport()
        x.credentials = (username, password)
        if rpc[1] in self.local_methods():
            self.log.info(('Proxy selecting local method for call to {0}').format(rpc[1]))
            server = XMLRPCServer(self, self.parent._protocol_dict['RPC2'], context=self.context, request=self.request)
            server.do_POST()
            return
        else:
            self.log.info(('Proxy calling remote method for call to {0}').format(rpc[1]))
            if self.context.user_agent_description['omphalos']['associativeLists']:
                if rpc[1].lower() == 'zogi.putobject':
                    args = disassociate_omphalos_representation(rpc[0])
                else:
                    args = rpc[0]
            else:
                args = rpc[0]
            server = xmlrpclib.Server(('http://{0}/zidestore/so/{1}/').format(Service.__ProxyHost__, username), transport=x)
            method = getattr(server, rpc[1])
            for attempt in range(1, 3):
                try:
                    result = method(*args)
                    break
                except xmlrpclib.ProtocolError, err:
                    self.log.warn('****Protocol Error, trying again in 0.5 seconds****')
                    self.log.exception(err)
                    time.sleep(0.5)
                except xmlrpclib.Fault, err:
                    self.log.warn('Fault code: %d' % err.faultCode)
                    self.log.warn('Fault string: %s' % err.faultString)
                    return
                except Exception, err:
                    self.log.exception(err)
                    request.send_response(500, 'XML-RPC Request Failed')
                    request.end_headers()
                    return

            if self.context.user_agent_description['omphalos']['associativeLists']:
                result = associate_omphalos_representation(result)
            result = xmlrpclib.dumps(tuple([result]), methodresponse=True)
            if Service.__PayloadTranscode__:
                self.log.debug('XML-RPC Proxy Transcoding Results')
                result = fix_microsoft_text(result)
            self.request.simple_response(200, data=result, mimetype='text/xml')
            return