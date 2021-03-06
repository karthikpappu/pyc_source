# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/tasksfolder.py
# Compiled at: 2012-10-12 07:02:39
import json
from StringIO import StringIO
from datetime import datetime, timedelta
from coils.foundation import CTag
from coils.core import Appointment
from coils.net import DAVFolder, OmphalosCollection, OmphalosObject, StaticObject, Parser, Multistatus_Response, CoilsException, NotImplementedException
from taskobject import TaskObject
from rss_feed import TasksRSSFeed
from groupwarefolder import GroupwareFolder
import coils.core.omphalos as omphalos
from coils.core.icalendar import Parser as VEvent_Parser

class TasksFolder(DAVFolder, GroupwareFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)
        self._start = None
        self._end = None
        return

    def get_property_webdav_owner(self):
        return ('<D:href>/dav/Contacts/{0}.vcf</D:href>').format(self.context.account_id)

    def get_property_webdav_resourcetype(self):
        return '<D:collection/><C:calendar/><G:vtodo-collection/>'

    def get_property_caldav_getctag(self):
        return self.get_ctag()

    def get_ctag(self):
        if self.is_collection_folder:
            return self.get_ctag_for_collection()
        else:
            return self.get_ctag_for_entity('Job')

    def get_property_caldav_supported_calendar_component_set(self):
        return unicode('<C:comp name="VTODO"/>')

    def _load_contents(self):
        self.log.info(('Loading content in task folder for name {0}').format(self.name))
        if self.is_collection_folder:
            result = None
            if self.is_project_folder:
                result = self.context.run_command('project::get-tasks', project=self.entity)
            if self.is_favorites_folder:
                raise NotImplementedException('Favoriting of tasks is not supported.')
            elif self.name == 'Delegated':
                result = self.context.run_command('task::get-delegated')
            elif self.name == 'ToDo':
                result = self.context.run_command('task::get-todo')
            elif self.name == 'Assigned':
                result = []
            elif self.name == 'Archived':
                result = self.context.run_command('task::get-archived')
            if result is None:
                return False
            self.data = {}
            if self._start is None:
                self._start = datetime.now() - timedelta(days=1)
            if self._end is None:
                self._end = datetime.now() + timedelta(days=90)
            for task in result:
                if self._start is not None or self._end is not None:
                    pass
                self.insert_child(task.object_id, task, alias=('{0}.ics').format(task.object_id))

        else:
            self.insert_child('Delegated', TasksFolder(self, 'Delegated', context=self.context, request=self.request))
            self.insert_child('ToDo', TasksFolder(self, 'ToDo', context=self.context, request=self.request))
            self.insert_child('Archived', TasksFolder(self, 'Archived', context=self.context, request=self.request))
            self.insert_child('Assigned', TasksFolder(self, 'Assigned', context=self.context, request=self.request))
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if name == '.ctag':
            if self.is_collection_folder:
                return self.get_ctag_representation(self.get_ctag_for_collection())
            else:
                return self.get_ctag_representation(self.get_ctag_for_entity('Job'))
        else:
            if name in ('.ls', '.json') and self.load_contents():
                return self.get_collection_representation(name, self.get_children())
            if name in ('.content.json', '.contents') and self.load_contents():
                return self.get_collection_representation(name, self.get_children(), rendered=True)
            location = None
            if self.is_collection_folder:
                if self.load_contents() and auto_load_enabled:
                    task = self.get_child(name)
                    location = ('/dav/Tasks/{0}').format(name)
            else:
                self.load_contents()
                result = self.get_child(name)
                if result is not None:
                    return result
                (object_id, payload_format, task, values) = self.get_task_for_key(name)
            if task is not None:
                return self.get_entity_representation(name, task, location=location, is_webdav=is_webdav)
        self.no_such_path()
        return

    def do_OPTIONS(self):
        """ Return a valid WebDAV OPTIONS response """
        methods = [
         'OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, COPY, MOVE',
         'PROPFIND, PROPPATCH, LOCK, UNLOCK, REPORT, ACL']
        self.request.simple_response(200, data=None, mimetype='text/plain', headers={'DAV': '1, 2, access-control, calendar-access', 'Allow': (',').join(methods), 
           'Connection': 'close', 
           'MS-Author-Via': 'DAV'})
        return

    def do_REPORT(self):
        """ Preocess a report request """
        payload = self.request.get_request_payload()
        self.log.debug('REPORT REQUEST: %s' % payload)
        parser = Parser.report(payload, self.context.user_agent_description)
        if parser.report_name == 'calendar-query':
            self._start = parser.parameters.get('start', None)
            self._end = parser.parameters.get('end', None)
            if self.load_contents():
                resources = []
                for child in self.get_children():
                    resources.append(TaskObject(self, child.get_file_name(), entity=child, location=('/dav/Tasks/{0}').format(child.get_file_name()), context=self.context, request=self.request))

                stream = StringIO()
                (properties, namespaces) = parser.properties
                Multistatus_Response(resources=resources, properties=properties, namespaces=namespaces, stream=stream)
                self.request.simple_response(207, data=stream.getvalue(), mimetype='text/xml; charset=utf-8')
        elif parser.report_name == 'calendar-multiget':
            resources = []
            self.log.info(('Found {0} references in multiget').format(len(parser.references)))
            for href in parser.references:
                try:
                    key = href.split('/')[(-1)]
                    resources.append(self.get_object_for_key(key))
                except NoSuchPathException, e:
                    self.log.debug(('Missing resource {0} in collection').format(key))
                except Exception, e:
                    self.log.exception(e)
                    raise e

            stream = StringIO()
            (properties, namespaces) = parser.properties
            Multistatus_Response(resources=resources, properties=properties, namespaces=namespaces, stream=stream)
            self.request.simple_response(207, data=stream.getvalue(), mimetype='text/xml; charset=utf-8')
        else:
            raise CoilsException(('Unsupported report {0} in {1}').format(parser.report_name, self))
        return

    def apply_permissions(self, task):
        pass

    def do_PUT(self, name):
        """ Process a PUT request """
        self.log.debug(('PUT request with name {0}').format(name))
        if_etag = self.request.headers.get('If-Match', None)
        if if_etag is None:
            self.log.warn('Client issued a put operation with no If-Match!')
        else:
            self.log.warn(('If-Match test not implemented at {0}').format(self.url))
        (format, extension, uid, name_is_numeric) = self.inspect_name(name, default_format='ics')
        print ('Format: {0} Extension: {1} UID: {2} Numeric: {3}').format(format, extension, uid, name_is_numeric)
        payload = self.request.get_request_payload()
        if format == 'ics':
            payload = VEvent_Parser.Parse(payload, self.context)
        else:
            raise NotImplementedException(('PUT of object format "{0}" not implemented').format(format))
        if len(payload) == 1:
            payload = payload[0]
            if 'caldav_uid' in payload:
                uid = payload['caldav_uid']
            task = self.context.run_command('task::get', uid=uid)
            if not task:
                if name_is_numeric:
                    task = self.context.run_command('task::get', id=int(name))
                task = task or self.context.run_command('task::new', values=payload)
                self.apply_permissions(task)
                self.context.commit()
                self.request.simple_response(201, data=None, mimetype='text/calendar; charset=utf-8', headers={'Etag': ('{0}:{1}').format(task.object_id, task.version), 'Location': ('/dav/Tasks/{0}').format(task.get_file_name())})
            else:
                task = self.context.run_command('task::set', object=task, values=payload)
                self.context.commit()
                self.request.simple_response(204, data=None, mimetype='text/calendar; charset=utf-8', headers={'Etag': ('{0}:{1}').format(task.object_id, task.version), 'Location': ('/dav/Tasks/{0}').format(task.get_file_name())})
        else:
            raise NotImplementedException('Multi-PUT not implemented, and not standard.')
        return

    def do_POST(self):

        def encode(o):
            if isinstance(o, datetime):
                return o.strftime('%Y-%m-%dT%H:%M:%S')
            raise TypeError()

        mimetype = self.request.headers.get('Content-Type', None)
        detail_level = 65503
        if mimetype == 'application/json':
            payload = self.request.get_request_payload()
            values = json.loads(payload)
            entity_name = values.get('entityName', None)
            if entity_name is None:
                raise CoilsException('JSON content must specify an Omphalos entityName value')
            elif entity_name == 'Task':
                try:
                    object_id = int(values.get('objectId', 0))
                except:
                    raise CoilsException(('Payload contained invalid objectId value "{0}"').format(values.get('objectId')))
                else:
                    if object_id == 0:
                        task = self.context.run_command('task::new', values=values)
                    else:
                        task = self.context.run_command('task::get', id=object_id)
                        if task is None:
                            raise CoilsException(('No such task as objectId#{0} available').format(object_id))
                        else:
                            self.context.run_command('task::set', values=values, object=task)
                    result = task
            elif entity_name == 'taskNotation':
                try:
                    object_id = None
                    object_id = int(values.get('taskObjectId'))
                except:
                    raise CoilsException(('Payload contained invalid objectId value "{0}"').format(values.get('objectId')))
                else:
                    task = self.context.run_command('task::get', id=object_id)
                    if task is None:
                        raise CoilsException(('No such task as objectId#{0} available').format(object_id))
                    else:
                        self.context.run_command('task::comment', values=values, task=task)
                    result = task
            elif entity_name == '_search':
                if 'criteria' in values:
                    detail_level = values.get('detailLevel', 0)
                    size_limit = int(values.get('limit', 150))
                    criteria = values.get('criteria')
                    result = self.context.run_command('task::search', criteria=criteria, limit=size_limit)
            else:
                raise NotImplementedException(('JSON POST of "{0}" entity not implemented').format(entity_name))
            self.context.commit()
            representation = omphalos.Render.Result(result, detail_level, self.context)
            if isinstance(result, list):
                headers = {}
            else:
                headers = {'Etag': ('{0}:{1}').format(task.object_id, task.version), 'X-COILS-OBJECT-ID': task.object_id}
            self.request.simple_response(200, data=json.dumps(representation, default=encode), mimetype='application/json; charset=utf-8', headers=headers)
        else:
            raise NotImplementedException(('POST of content-type "{0}" not implemented').format(mimetype))
        return