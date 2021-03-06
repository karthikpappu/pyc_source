# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/ammunition/tracker.py
# Compiled at: 2016-07-19 22:50:03
"""define tracker for tracer use.

"""
import logging, time, random, sys, traceback
from tingyun.armoury.ammunition.timer import Timer
from tingyun.battlefield.knapsack import knapsack
from tingyun.logistics.warehouse.database_node import DatabaseNode
from tingyun.logistics.warehouse.tracker_node import TrackerNode
from tingyun.logistics.warehouse.error_node import ErrorNode, ExternalErrorNode
from tingyun.packages import six
console = logging.getLogger(__name__)

class Tracker(object):
    """Tracker, the battle entrance.
    """

    def __init__(self, proxy, enabled=None, framework='Python'):
        """
        :param proxy: communication proxy instance to controller.
        :return:
        """
        self.framework = framework
        self.proxy = proxy
        self.enabled = False
        self._settings = None
        self.thread_id = knapsack().current_thread_id()
        self.background_task = False
        self.start_time = 0
        self.end_time = 0
        self.queque_start = 0
        self._queque_time = 0
        self.trace_node = []
        self.async_func_trace_time = 0
        self._errors = []
        self.external_error = []
        self._custom_params = {}
        self._slow_sql_nodes = []
        self.http_method = 'GET'
        self.request_uri = None
        self.http_status = 500
        self.request_params = {}
        self.header_params = {}
        self.cookie_params = {}
        self._priority = 0
        self._group = None
        self._name = None
        self.apdex = 0
        self._frozen_path = None
        self.stack_trace_count = 0
        self.explain_plan_count = 0
        self.thread_name = 'Unknown'
        self.referer = ''
        self._trace_guid = ''
        self._trace_id = ''
        self._tingyun_id = ''
        self._called_traced_data = ''
        self.call_tingyun_id = ''
        self.call_req_id = ''
        self.db_time = -1
        self.external_time = -1
        self.redis_time = -1
        self.memcache_time = -1
        self.mongo_time = -1
        global_settings = proxy.global_settings
        if global_settings.enabled:
            if enabled or enabled is None and proxy.enabled:
                self._settings = proxy.settings
                if not self._settings:
                    self.proxy.activate()
                    self._settings = proxy.settings
                if self._settings:
                    self.enabled = True
        if self.enabled:
            self._tingyun_id = self._settings.tingyunIdSecret
        return

    def __enter__(self):
        """
        :return:
        """
        if not self.enabled:
            return self
        else:
            try:
                self.save_tracker()
            except Exception as _:
                console.fatal('Fatal error when save tracker. if this continues. please contact us for further                            investigation')
                raise

            self.start_time = time.time()
            self.trace_node.append(Timer(None))
            return

    def __exit__(self, exc_type, exc_val, exc_tb, async=False):
        """
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :param async: in tornado, the tracker is not saved in thread cache
        :return:
        """
        if not self.enabled:
            return
        else:
            if not async:
                try:
                    self.drop_tracker()
                except Exception as err:
                    console.exception('error detail %s', err)
                    raise

            if not self.is_uri_captured(self.request_uri):
                console.debug('ignore the uri %s', self.request_uri)
                return
            if exc_type is not None and exc_val is not None and exc_tb is not None:
                self.record_exception(exc_type, exc_val, exc_tb)
            self.end_time = time.time()
            duration = self.duration
            root_node = self.trace_node.pop()
            children = root_node.children
            exclusive = duration + root_node.exclusive
            tracker_type = 'WebAction' if not self.background_task else 'BackgroundAction'
            group = self._group or ('Python' if self.background_task else 'Uri')
            request_params = self.filter_params(self.request_params)
            uri = self.url_encode(self.request_uri)
            apdex_t = self._settings.apdex_t
            path = self.path
            if path in self._settings.action_apdex:
                apdex_t = self._settings.action_apdex.get(path)
            node = TrackerNode(type=tracker_type, group=group, name=self._name, start_time=self.start_time, end_time=self.end_time, request_uri=uri, duration=duration, thread_name=self.thread_name, http_status=self.http_status, exclusive=exclusive, children=tuple(children), path=self.path, errors=self._errors, apdex_t=apdex_t, queque_time=self.queque_time, custom_params=self._custom_params, request_params=request_params, trace_id=self._trace_id, referer=self.referer, slow_sql=self._slow_sql_nodes, trace_guid=self.generate_trace_guid(), trace_data=self._called_traced_data, external_error=self.external_error)
            self.proxy.record_tracker(node)
            return

    def record_exception(self, exc=None, value=None, tb=None, params=None, tracker_type='WebAction', ignore_errors=[]):
        """ record the exception for trace
        :param exc:
        :return:
        """
        if not self._settings or not self._settings.error_collector.enabled:
            return
        if exc is None and value is None and tb is None:
            exc, value, tb = sys.exc_info()
        if exc is None or value is None or tb is None:
            console.warning('None exception is got. skip it now. %s, %s, %s', exc, value, tb)
            return
        else:
            if self.http_status in self._settings.error_collector.ignored_status_codes:
                console.debug('ignore the status code %s', self.http_status)
                return
            if callable(ignore_errors):
                should_ignore = ignore_errors(exc, value, tb, self._settings.error_collector.ignored_status_codes)
                if should_ignore:
                    return
            if self.http_status in self._settings.error_collector.ignored_status_codes:
                console.debug('record_exception: ignore  error collector status code')
                return
            module = value.__class__.__module__
            name = value.__class__.__name__
            fullname = '%s:%s' % (module, name) if module else name
            request_params = self.filter_params(self.request_params)
            if params:
                custom_params = dict(request_params)
                custom_params.update(params)
            else:
                custom_params = dict(request_params)
            try:
                message = str(value)
            except Exception as _:
                try:
                    message = six.text_type(value)
                except Exception as _:
                    message = '<unprintable %s object>' % type(value).__name__

            stack_trace = traceback.extract_tb(tb)
            node = ErrorNode(error_time=int(time.time()), http_status=self.http_status, error_class_name=fullname, uri=self.url_encode(self.request_uri), thread_name=self.thread_name, message=message, stack_trace=stack_trace, request_params=custom_params, tracker_type=tracker_type, referer=self.referer)
            self._errors.append(node)
            return

    def record_external_error(self, url, error_code, http_status=0, _exception=None, request_params=None, tracker_type='External'):
        """
        :return:
        """
        ignored_status = [
         401]
        if http_status in ignored_status or int(http_status) < 400:
            console.info('Agent caught http status code %s, ignore it now.', http_status)
            return
        status_code = error_code or http_status
        error_class_name = ''
        stack_trace = ''
        if _exception:
            exc, value, tb = _exception
            module = value.__class__.__module__
            name = value.__class__.__name__
            error_class_name = '%s:%s' % (module, name) if module else name
            stack_trace = traceback.extract_tb(tb)
        node = ExternalErrorNode(error_time=int(time.time()), status_code=status_code, thread_name=self.thread_name, url=url, error_class_name=error_class_name, http_status=http_status, stack_trace=stack_trace, request_params=request_params, tracker_type=tracker_type)
        self.external_error.append(node)

    @property
    def path(self):
        """the call tree path
        """
        if self._frozen_path:
            return self._frozen_path
        else:
            if not self.background_task:
                tracker_type = 'WebAction' if 1 else 'BackgroundAction'
                name = self._name or 'Undefined'
                try:
                    named_metric = self.settings.naming.naming_web_action(self.http_method, self.request_uri, self.request_params, self.header_params, self.cookie_params)
                except Exception as err:
                    console.error('Error occurred when parsing naming rules. %s', err)
                    named_metric = None

                if named_metric:
                    path = '%s/%s' % (tracker_type, self.url_encode(named_metric))
                    return path
                uri_params_captured = self._settings.web_action_uri_params_captured.get(self.request_uri, '')
                if self.request_uri in self._settings.web_action_uri_params_captured:
                    match_param = ''
                    for actual_param in self.request_params:
                        if actual_param in uri_params_captured:
                            match_param += '&%s=%s' % (actual_param, self.request_params[actual_param])

                    match_param = match_param.replace('&', '?', 1)
                    self.request_uri = '%s%s' % (self.request_uri, match_param)
                path = self._settings.auto_action_naming or '%s/%s/%s' % (tracker_type, self.framework, self.url_encode(self.request_uri))
            else:
                path = '%s/%s/%s' % (tracker_type, self.framework, name)
            return path

    def url_encode(self, uri):
        """
        :param uri:
        :return:
        """
        encoded_url = 'index'
        if not uri or uri == '/':
            return encoded_url
        uri = self.merge_urls(uri.replace('/', '', 1))
        encoded_url = uri.replace('/', '%2F')
        return encoded_url

    def merge_urls(self, url):
        """
        :param url:
        :return:
        """
        if not self.settings.urls_merge or self.settings.auto_action_naming:
            return url

        def is_digit(world):
            if str(world).isdigit():
                return '*'
            return world

        url_re = ('/').join([ is_digit(s) for s in url.split('/') ])
        url_segments = []
        pre_is_digit = False
        is_param = False
        for s in str(url_re):
            if s == '?':
                is_param = True
            if is_param:
                url_segments.append(s)
                continue
            if str(s).isdigit() and pre_is_digit:
                url_segments[-1] = '*'
            elif str(s).isdigit() and not pre_is_digit:
                pre_is_digit = True
                url_segments.append(s)
            else:
                url_segments.append(s)
                pre_is_digit = False

        return ('').join(url_segments)

    def set_tracker_name(self, name, group='Function', priority=None):
        """used to consist metric identification
        """
        if priority is None:
            return
        else:
            if priority is not None and priority < self._priority:
                return
            if isinstance(name, bytes):
                name = name.decode('Latin-1')
            self._priority = priority
            self._group = group
            self._name = name
            return

    def save_tracker(self):
        knapsack().save_tracker(self)

    def drop_tracker(self):
        if not self.enabled:
            return self
        knapsack().drop_tracker(self)

    def process_database_node(self, node):
        """record the database node
        :param node: database node
        :return:
        """
        if type(node) is not DatabaseNode:
            return
        if not self._settings.action_tracer.enabled:
            return
        if not self._settings.action_tracer.slow_sql:
            return
        if self._settings.action_tracer.record_sql == 'off':
            return
        if node.duration < self._settings.action_tracer.slow_sql_threshold:
            return
        self._slow_sql_nodes.append(node)

    def push_node(self, node):
        self.trace_node.append(node)

    def pop_node(self, node):
        """return parent trace node
        """
        last = self.trace_node.pop()
        assert last == node
        parent = self.trace_node[(-1)]
        return parent

    def current_node(self):
        """
        """
        if self.trace_node:
            return self.trace_node[(-1)]

    def is_uri_captured(self, uri):
        """check the uri is captured or not
        :param uri: uri of the request
        :return: True, if it's need to captured. else return False
        """
        if not self._settings.urls_captured:
            return True
        for p in self._settings.urls_captured:
            if p and p.match(uri):
                return True

        return False

    def filter_params(self, params):
        """filter the parameters
        :param params: the dict parameters
        :return: filtered parameters
        """
        result = {}
        if not params:
            return result
        if not self._settings.action_tracer.enabled or not self._settings.capture_params:
            return result
        for key in params:
            if key not in self._settings.ignored_params:
                result[key] = params[key]

        return result

    @property
    def name(self):
        return self._name

    @property
    def group(self):
        return self._group

    @property
    def settings(self):
        return self._settings

    @property
    def duration(self):
        """
        :return:
        """
        if not self.end_time:
            self.end_time = time.time()
        return int((self.end_time - self.start_time) * 1000)

    def generate_trace_guid(self):
        """
        :return:
        """
        duration = self.duration
        if duration < self.settings.action_tracer.stack_trace_threshold:
            return ''
        if self._trace_guid:
            return self._trace_guid
        guid = '%s%s' % (time.time(), random.random())
        guid = guid.replace('.', '')
        self._trace_guid = guid[:30]
        return self._trace_guid

    def generate_trace_id(self):
        """
        :return:
        """
        if self._trace_id:
            return self._trace_id
        trace_id = '%s%s' % (time.time(), random.random())
        trace_id = trace_id.replace('.', '')
        self._trace_id = trace_id[:16]
        return self._trace_id

    @property
    def queque_time(self):
        """
        :return:
        """
        if not self._queque_time:
            _queque_time = int(self.start_time * 1000.0 - self.queque_start)
            self._queque_time = _queque_time if _queque_time > 0 and self.queque_start != 0 else 0
        return self._queque_time


def current_tracker():
    """return current tracker in the thread
    :return:
    """
    return knapsack().current_tracker()