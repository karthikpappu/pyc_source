# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snurtle/rpcclient.py
# Compiled at: 2012-08-06 14:04:27
import Queue, uuid
from threading import Thread
from jsonrpc import JSONRPCClient

class CaseInsensitiveDict(dict):

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            value = CaseInsensitiveDict().update(value)
        super(CaseInsensitiveDict, self).__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(key.lower())

    def set(self, key, value):
        self[key.lower()] = value

    def get(self, key, default):
        if key.lower() in self:
            return self[key.lower()]
        else:
            return default

    def update(self, in_):
        for key, value in in_.items():
            if key == 'FLAGS':
                pass
            elif isinstance(value, list):
                result = []
                for x in value:
                    if isinstance(x, dict):
                        z = CaseInsensitiveDict()
                        z.update(x)
                        value = z
                    elif isinstance(x, list):
                        value = z
                    result.append(value)

                value = result
            self.set(key, value)


class RPCDict(CaseInsensitiveDict):
    pass


class RPCError(object):

    def __init__(self, callid, error, state):
        self._error = error
        self.callid = callid
        self.state = state

    def __repr__(self):
        return ('<RPCError "{0}">').format(self._error)


class RPCResponse(object):

    def __init__(self, callid, data, state):
        self.callid = callid
        self.state = state
        self._set_data(data)

    def _set_data(self, data):
        if isinstance(data, list):
            self._data = []
            for v_ in data:
                if isinstance(v_, dict):
                    i = RPCDict()
                    i.update(v_)
                else:
                    i = v_
                self._data.append(i)

        elif isinstance(data, dict):
            self._data = RPCDict()
            self._data.update(data)
        else:
            self._data = data

    @property
    def payload(self):
        return self._data

    def __repr__(self):
        return ('<RPCResponse callid="{0}" payload="{1}">').format(self.callid, type(self.payload))


class RPCClient(object):

    def __init__(self, uri, credentials):
        self._queue = Queue.Queue(maxsize=4096)
        self.rpc_handler = JSONRPCClient(uri, credentials=credentials)

    def run(self):
        self._running = True
        self._worker = Thread(target=self.work)
        self._worker.start()
        self._worker.join(0.1)

    @property
    def running(self):
        return self._running

    def stop(self):
        self._queue.put('STOP:')

    def call(self, method, params, callback, state, feedback):
        call_id = uuid.uuid4().hex
        self._queue.put({'method': method, 'params': params, 
           'callback': callback, 
           'callid': call_id, 
           'feedback': feedback, 
           'state': state})
        if feedback:
            feedback(('client: callId#{0} queued').format(call_id))
        return call_id

    def work(self):
        while self.running:
            call = None
            try:
                call = self._queue.get(True, timeout=15)
            except Queue.Empty:
                pass

            if call:
                if isinstance(call, basestring):
                    if call == 'STOP:':
                        self._running = False
                elif isinstance(call, dict):
                    if call['feedback']:
                        call['feedback'](('client: calling {0} with params {1}').format(call['method'], call['params']))
                    try:
                        result = self.rpc_handler.call(call['method'], call['params'], call['callid'])
                    except Exception as e:
                        if call['callback']:
                            call['callback'](RPCError(call['callid'], e, call['state']))
                    else:
                        if call['callback']:
                            call['callback'](RPCResponse(call['callid'], result, call['state']))

        return

    def authenticate(self):
        call_id = uuid.uuid4().hex
        try:
            result = self.rpc_handler.call('getLoginAccount', [
             0], call_id)
        except:
            return False

        if isinstance(result, dict):
            return (result['objectId'], result['login'])
        return False

    def get_objects_by_id(self, fetchids=None, detail=0, callback=None, state=None, feedback=None):
        return self.call('getObjectsById', [
         fetchids, detail], callback, state, feedback)

    def get_object_by_id(self, fetchid=None, detail=0, callback=None, state=None, feedback=None):
        return self.call('getObjectById', [
         fetchid, detail], callback, state, feedback)

    def get_type_of_object(self, fetchid=None, callback=None, state=None, feedback=None):
        return self.call('getTypeOfObject', [
         fetchid], callback, state, feedback)

    def search_for_objects(self, entity=None, criteria=None, detail=0, callback=None, state=None, feedback=None):
        return self.call('searchForObjects', [
         entity, criteria, detail], callback, state, feedback)

    def get_login_account(self, detail=0, callback=None, state=None, feedback=None):
        return self.call('getLoginAccount', [
         detail], callback, state, feedback)

    def put_object(self, payload=None, callback=None, state=None, feedback=None):
        tmp = {}
        tmp.update(payload)
        if 'objectid' in tmp:
            tmp['objectId'] = tmp['objectid']
        return self.call('putObject', [
         tmp], callback, state, feedback)

    def delete_object(self, objectid=None, payload=None, callback=None, state=None, feedback=None):
        if objectid:
            return self.call('deleteObject', [
             objectid], callback, state, feedback)
        else:
            return self.call('deleteObject', [
             payload], callback, state, feedback)

    def get_favorites(self, entity_name=None, detail_level=0, callback=None, state=None, feedback=None):
        return self.call('getFavoritesByType', [
         entity_name, detail_level], callback, state, feedback)

    def favorite(self, objectids=None, callback=None, state=None, feedback=None):
        return self.call('flagFavorites', [
         objectids], callback, state, feedback)

    def unfavorite(self, objectids=None, callback=None, state=None, feedback=None):
        return self.call('unflagFavorites', [
         objectids], callback, state, feedback)

    def get_performance(self, category=None, callback=None, state=None, feedback=None):
        return self.call('getPerformance', [
         category], callback, state, feedback)

    def get_process_list(self, callback=None, state=None, feedback=None):
        return self.call('ps', [], callback, state, feedback)