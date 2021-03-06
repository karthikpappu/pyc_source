# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/xmppBus.py
# Compiled at: 2018-09-24 09:11:49
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import socket, logging, traceback, urllib, pickle, sleekxmpp, busIndipendentMessages, xmppMessages, bus, sys, time

class XMPPBus(bus.Bus):

    def __init__(self, config, service_name, service_name_namespace, id='master'):
        bus.Bus.__init__(self, id)
        self.config = config
        self.address = (config.get('DEFAULT', 'address'), config.get('DEFAULT', 'port'))
        self.domain = config.get('DEFAULT', 'domain')
        self.MUC_name = config.get('DEFAULT', 'mucService')
        self.username = config.get('DEFAULT', 'user')
        self.password = config.get('DEFAULT', 'password')
        self.nameSpacePassword = config.get('DEFAULT', 'mucServicePassword')
        self._service_name = service_name
        self._service_name_namespace = service_name_namespace
        self._fully_qualified_service_name = self._service_name_namespace + '.' + self._service_name
        self.xmpp = sleekxmpp.ClientXMPP(self._get_JId(), self.password)
        self.xmpp.register_plugin('xep_0004')
        self.xmpp.register_plugin('xep_0030')
        self.xmpp.register_plugin('xep_0045')
        self.xmpp.register_plugin('xep_0060')
        self.xmpp.register_plugin('xep_0077')
        self.xmpp.register_plugin('xep_0078')
        self.xmpp.register_plugin('xep_0199')
        self.xmpp.register_plugin('xep_0249')
        self.xmpp.add_event_handler('register', self._register)
        self.xmpp.add_event_handler('session_start', self._startService)
        self.xmpp.add_event_handler('message', self._handleXMPPSignal)

    def clone_for_process(self, id):
        c = XMPPBus(self.config, self._service_name, self._service_name_namespace, id)
        return c

    def _get_JId(self):
        return ('').join([self.username, '@', self.domain, '/', self.id, '@', socket.gethostname()])

    def _get_MUC_JId(self):
        return self._service_name_namespace + '@' + self.MUC_name

    def _MUC_service_nickname(self):
        return '%s@%s' % (self._service_name, str(self.xmpp.boundjid).split('@', 1).pop())

    def CheckServerIdentity(self, serverId):
        pass

    def get_fully_qualified_service_name(self):
        return self._fully_qualified_service_name

    def Listen(self):
        logging.info('Trying to connect...')
        for x in xrange(5):
            if self.xmpp.connect(self.address, use_tls=False, use_ssl=True):
                logging.info('State: %s' % str(self.state()))
                if self.state() == 'connected':
                    try:
                        try:
                            self.xmpp.send_presence()
                            self.xmpp.process(block=True)
                            break
                        except:
                            stack_trace = traceback.format_exc(sys.exc_info())
                            logging.exception('Service ' + str(self._service_name) + ' Exception: ' + str(stack_trace))

                    finally:
                        self.xmpp.disconnect()

                else:
                    logging.info('Cannot connect to xmpp server. Tentative # ' + str(x + 1))
                    time.sleep(2)

    def _startService(self, event):
        self.JoinMUC()

    def JoinMUC(self):
        self.xmpp.plugin['xep_0045'].joinMUC(self._get_MUC_JId(), self._MUC_service_nickname(), password=self.nameSpacePassword)

    def _handleXMPPSignal(self, msg):
        imsg = self.CreateIndipendentMessage(msg)
        if imsg is not None:
            self.callbacks[type(imsg)](imsg)
        return

    def CreateIndipendentMessage(self, msg):
        if msg['type'] in ('normal', 'chat'):
            payload = msg['body']
            origin = msg['from']
            logging.info('Received XMPP bus signal from %s: "%s"' % (origin, payload))
            role = 'visitor'
            roster = self.xmpp.plugin['xep_0045'].getRoster(self._get_MUC_JId())
            if origin.resource in roster:
                role = self.xmpp.plugin['xep_0045'].rooms[self._get_MUC_JId()][origin.resource]['role']
            elif origin.user in roster:
                role = self.xmpp.plugin['xep_0045'].rooms[self._get_MUC_JId()][origin.user]['role']
            logging.info('handle message from WPS Role ' + str(role))
            if role != 'visitor':
                if 'topic=request' in payload:
                    logging.info('handle request message from WPS ' + str(payload))
                    variables = dict([ tuple(each.strip().split('=')) for each in payload.split('&') ])
                    requestParams = pickle.loads(urllib.unquote(variables['message'])) if variables['message'] is not None else None
                    return busIndipendentMessages.ExecuteMessage(msg['from'], variables['id'], variables['baseURL'], requestParams)
                if 'topic=invite' in payload:
                    logging.info('handle invite message from WPS ' + str(payload))
                    return busIndipendentMessages.InviteMessage(payload, msg['from'])
                if 'topic=finish' in payload:
                    logging.info('handle finish message from WPS ' + str(payload))
                    return busIndipendentMessages.FinishMessage(payload, msg['from'])
                if 'topic=abort' in payload:
                    logging.info('handle abort message from WPS ' + str(payload))
                    return busIndipendentMessages.AbortMessage(payload, msg['from'])
                if 'topic=getloadavg' in payload:
                    return busIndipendentMessages.GetLoadAverageMessage(payload, msg['from'])
        return

    def SendMessage(self, message):
        m = self.Convert(message)
        m.send()

    def Stop(self, Message):
        pass

    def _register(self, iq):
        pass

    def Convert(self, busIndipendentMsg):
        if type(busIndipendentMsg) is busIndipendentMessages.RegisterMessage:
            return xmppMessages.XMPPRegisterMessage(self, busIndipendentMsg.originator(), busIndipendentMsg.service, busIndipendentMsg.namespace, busIndipendentMsg.description, busIndipendentMsg.input_parameters(), busIndipendentMsg.output)
        if type(busIndipendentMsg) is busIndipendentMessages.ProgressMessage:
            return xmppMessages.XMPPProgressMessage(busIndipendentMsg.originator, self, busIndipendentMsg.progress)
        if type(busIndipendentMsg) is busIndipendentMessages.LogMessage:
            return xmppMessages.XMPPLogMessage(busIndipendentMsg.originator, self, busIndipendentMsg.level, busIndipendentMsg.msg)
        if type(busIndipendentMsg) is busIndipendentMessages.CompletedMessage:
            return xmppMessages.XMPPCompletedMessage(busIndipendentMsg.originator, self, busIndipendentMsg.base_url, busIndipendentMsg.outputs())
        if type(busIndipendentMsg) is busIndipendentMessages.ErrorMessage:
            return xmppMessages.XMPPErrorMessage(busIndipendentMsg.originator, self, busIndipendentMsg.msg, busIndipendentMsg.id)
        if type(busIndipendentMsg) is busIndipendentMessages.AbortMessage:
            return xmppMessages.XMPPErrorMessage(busIndipendentMsg.originator, self, busIndipendentMsg.msg, busIndipendentMsg.id)
        if type(busIndipendentMsg) is busIndipendentMessages.LoadAverageMessage:
            return xmppMessages.XMPPLoadAverageMessage(busIndipendentMsg.originator, self, busIndipendentMsg.outputs())
        raise Exception('unknown message')

    def disconnect(self):
        self.xmpp.disconnect(wait=True)

    def state(self):
        return self.xmpp.state.current_state()