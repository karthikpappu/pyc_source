# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snurtle/shell.py
# Compiled at: 2012-09-10 09:50:00
import getpass, threading, time, sys
from cmd2 import Cmd, options, make_option
from mako.template import Template
from rpcclient import RPCClient, RPCResponse, RPCError, RPCDict, CaseInsensitiveDict
from version import __version__
from bundles.task import TaskCLIBundle
from bundles.common import CommonCLIBundle
from bundles.route import RouteCLIBundle
from bundles.process import ProcessCLIBundle
from bundles.project import ProjectCLIBundle
from bundles.contact import ContactCLIBundle
from bundles.collection import CollectionCLIBundle
from bundles.enterprise import EnterpriseCLIBundle
from bundles.team import TeamCLIBundle
from config import Configuration

class Shell(Cmd, CommonCLIBundle, TaskCLIBundle, RouteCLIBundle, ProcessCLIBundle, ProjectCLIBundle, EnterpriseCLIBundle, CollectionCLIBundle, ContactCLIBundle, TeamCLIBundle):
    server = None
    _current = None
    _previous = None
    _template = None
    propmt = ':> '
    quiet = True
    login = None
    hostname = None
    secure = 0

    def __init__(self, config):
        Cmd.__init__(self)
        self._config = config
        Cmd.settable.append('login')
        Cmd.settable.append('hostname')
        Cmd.settable.append('secure')
        self._import_configuration()

    @property
    def configuration(self):
        return self._config

    def _import_configuration(self):
        self.login = Configuration.GetLogin(self.configuration)
        self.hostname = Configuration.GetHost(self.configuration)
        self.secure = Configuration.GetSecure(self.configuration)

    def _export_configuration(self):
        Configuration.SetLogin(self.configuration, self.login)
        Configuration.SetHost(self.configuration, self.hostname)
        Configuration.SetSecure(self.configuration, self.secure)

    def set_result(self, result, error=False, template=None, header=None):
        self._current = result
        self._error = error
        self._template = template
        self._header = header

    @property
    def current_result(self):
        return self._current

    def complete_result(self):
        self.pfeedback('shell: completing result')
        self._previous = self._current
        self._current = None
        self._template = None
        return

    lock = threading.Lock()
    event = threading.Event()
    responses = {}

    def callback(self, response_):
        self.lock.acquire()
        self.pfeedback('callback: response lock acquired')
        self.pfeedback(('callback: received response to callId#{0}').format(response_.callid))
        self.responses[response_.callid] = response_
        self.pfeedback('callback: triggering event')
        self.event.set()
        self.pfeedback('callback: clearing event')
        self.event.clear()
        self.lock.release()
        self.pfeedback('callback: response lock released')

    def get_response(self, callid, nowait=False, timeout=60, delete=True):
        self.lock.acquire()
        self.pfeedback('get-response: response lock acquired')
        response = self.responses.get(callid, None)
        self.lock.release()
        self.pfeedback('get-response: response lock released')
        if not response:
            self.pfeedback(('get-response: response not yet received for callId#{0}').format(callid))
            if nowait:
                pass
            else:
                end_time = time.time() + timeout
                while not response and time.time() < end_time:
                    self.pfeedback(('get-response: waiting for response or timeout @ {0}').format(end_time))
                    duration = end_time - time.time()
                    if duration < 1.0:
                        duration = 1.0
                    self.event.wait(duration)
                    self.pfeedback('get-response: event triggered or time-out reached')
                    self.lock.acquire()
                    self.pfeedback('get-response: response lock acquired')
                    response = self.responses.get(callid, None)
                    if response:
                        self.pfeedback('get-response: response found')
                        if delete:
                            self.pfeedback('get-response: removing response from response dict')
                            del self.responses[callid]
                        else:
                            self.pfeedback('get-response: response to call remains in response dict')
                    else:
                        self.pfeedback('get-response: response not found')
                    self.lock.release()
                    self.pfeedback('get-response: response lock released')

        return response

    def server_ok(self):
        if not self.server:
            self.set_result('No authenticated server connection', error=True)
            return False
        return True

    def postcmd(self, stop, line):
        result = self.current_result
        self.pfeedback(('postcmd: result for command is of type {0}').format(type(result)))
        if result:
            if isinstance(result, RPCResponse):
                self.pfeedback('postcmd: payload selected as result from RPCResponse')
                result = result.payload
                self.pfeedback(('postcmd: payload is of type {0}').format(type(result)))
            if isinstance(result, list):
                self.pfeedback('postcmd: processing result as a list of objects')
                for x in result:
                    self._output_result(x, error=self._error)

            else:
                self.pfeedback('postcmd: processing result as a single object')
                self._output_result(result, error=self._error)
        else:
            self.pfeedback('postcmd: presenting no output for command')
        self.complete_result()
        return stop

    def _output_result(self, value, error=False):
        header = None
        if isinstance(value, basestring):
            value = value
        elif isinstance(value, bool):
            value = str(value)
        elif isinstance(value, RPCError):
            error = True
        elif isinstance(value, RPCDict) or isinstance(value, dict):
            if self._template:
                if self._header:
                    header = Template(self._header)
                self.pfeedback('output: using template to display object')
                value = Template(self._template).render(report=value)
                self.pfeedback('output: template processing complete')
            else:
                self.pfeedback('output: presenting default list form')
                header = ('{:^12} {:^30} ').format('objectId', 'entityName')
                value = ('{:<12} {:<30} ').format(value.get('objectid', None), value.get('entityname', None))
        elif isinstance(value, dict):
            if value.get('entityname', None) == 'message':
                self.pfeedback('output: presenting Message list form')
                value = ('Message {0} {1} {2} {3} {4}').format(value['uuid'], value['label'], value['mimetype'], value['size'], value['version'])
        if error:
            self.perror(value)
        else:
            if isinstance(header, basestring):
                self.poutput(header)
            if isinstance(value, basestring):
                self.poutput(value)
            else:
                self.perror(('value is not a string, but {0}').format(type(value)))
        return

    def do_authenticate(self, arg, opts=None):
        if self.login and self.hostname:
            secret = getpass.getpass('Password:')
            credentials = {'username': self.login, 'password': secret}
            if self.secure:
                uri = ('https://{0}/jsonrpc').format(self.hostname)
            else:
                uri = ('http://{0}/jsonrpc').format(self.hostname)
            server = RPCClient(uri, credentials=credentials)
            result = server.authenticate()
            if result:
                self.server = server
                self.context_id = result[0]
                self.prompt = ('{0}> ').format(result[1])
                self.server.run()
                self.set_result(('authenticated as contextId#{0} [login:{1}]').format(result[0], result[1]))
            else:
                self.set_result('authentication failure')

    def do_version(self, arg, opts=None):
        self.set_result(('Snurtle {0}').format(__version__))

    def do_disconnect(self, arg, opts=None):
        if self.server:
            self.server.stop()

    def do_quit(self, arg, opts=None):
        if self.server:
            self.pfeedback('disconnecting from server')
            self.server.stop()
        self._export_configuration()
        return Cmd.do_quit(self, arg)

    def interrupt_handler(self, signum, frame):
        print '<SIGINT/>'
        self.do_quit(None)
        sys.exit(0)
        return