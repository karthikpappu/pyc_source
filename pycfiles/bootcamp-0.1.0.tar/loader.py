# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/bootalchemy/loader.py
# Compiled at: 2013-01-29 22:57:23
from yaml import load
import sys, logging
from pprint import pformat
from converters import timestamp, timeonly
from sqlalchemy.orm import class_mapper
from sqlalchemy import Unicode, Date, DateTime, Time, Integer, Float, Boolean, String, Binary
try:
    from sqlalchemy.exc import IntegrityError
except ImportError:
    from sqlalchemy.exceptions import IntegrityError

from functools import partial
log = logging.Logger('bootalchemy', level=logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)
try:
    from sqlalchemy.dialects.postgresql.base import PGArray
except ImportError:
    log.error('You really should upgrade to SQLAlchemy=>0.6 to get the full bootalchemy experience')
    PGArray = None

class Loader(object):
    """
       Basic Loader

       *Arguments*
          model
            list of classes in your model.
          references
            references from an sqlalchemy session to initialize with.
          check_types
            introspect the target model class to re-cast the data appropriately.
    """
    default_encoding = 'utf-8'

    def cast(self, type_, cast_func, value):
        if type(value) == type_:
            return value
        else:
            return cast_func(value)

    def __init__(self, model, references=None, check_types=True):
        self.default_casts = {Integer: int, Unicode: partial(self.cast, unicode, lambda x: unicode(x, self.default_encoding)), 
           Date: timestamp, 
           DateTime: timestamp, 
           Time: timeonly, 
           Float: float, 
           Boolean: partial(self.cast, bool, lambda x: x.lower() not in ('f', 'false', 'no', 'n')), 
           Binary: partial(self.cast, str, lambda x: x.encode('base64'))}
        if PGArray:
            self.default_casts[PGArray] = list
        self.source = 'UNKNOWN'
        self.model = model
        if references is None:
            self._references = {}
        else:
            self._references = references
        if not isinstance(model, list):
            model = [
             model]
        self.modules = []
        for item in model:
            if isinstance(item, basestring):
                self.modules.append(__import__(item))
            else:
                self.modules.append(item)

        self.check_types = check_types
        return

    def clear(self):
        """
        clear the existing references
        """
        self._references = {}

    def create_obj(self, klass, item):
        """
        create an object with the given data
        """
        try:
            obj = klass(**item)
        except TypeError as e:
            self.log_error(e, None, klass, item)
            raise TypeError('The class, %s, cannot be given the items %s. Original Error: %s' % (
             klass.__name__, str(item), str(e)))
        except AttributeError as e:
            self.log_error(e, None, klass, item)
            raise AttributeError('Object creation failed while initializing a %s with the items %s. Original Error: %s' % (
             klass.__name__, str(item), str(e)))
        except KeyError as e:
            self.log_error(e, None, klass, item)
            raise KeyError('On key, %s, failed while initializing a %s with the items %s. %s.keys() = %s' % (
             str(e), klass.__name__, str(item), klass.__name__, str(klass.__dict__.keys())))

        return obj

    def resolve_value(self, value):
        """
        `value` is a string or list that will be applied to an ObjectName's attribute.
        Link in references when it hits a value that starts with an "*"
        Ignores values that start with an "&"
        Nesting also happens here: Create new objects for values that start with a "!"
        Recurse through lists.
        """
        if isinstance(value, basestring):
            if value.startswith('&'):
                return None
            if value.startswith('*'):
                if value[1:] in self._references:
                    return self._references[value[1:]]
                raise Exception('The pointer %(val)s could not be found. Make sure that %(val)s is declared before it is used.' % {'val': value})
        elif isinstance(value, dict):
            keys = value.keys()
            if len(keys) == 1 and keys[0].startswith('!'):
                klass_name = keys[0][1:]
                items = value[keys[0]]
                klass = self.get_klass(klass_name)
                if isinstance(items, dict):
                    return self.add_klass_with_values(klass, items)
                if isinstance(items, list):
                    return self.add_klasses(klass, items)
                raise TypeError('You can only give a nested value a list or a dict. You tried to feed a %s into a %s.' % (
                 items.__class__.__name__, klass_name))
        elif isinstance(value, list):
            return [ self.resolve_value(list_item) for list_item in value ]
        return value

    def has_references(self, item):
        for key, value in item.iteritems():
            if isinstance(value, basestring) and value.startswith('&'):
                return True

    def add_reference(self, key, obj):
        """
        add a reference to the internal reference dictionary
        """
        self._references[key[1:]] = obj

    def set_references(self, obj, item):
        """
        extracts the value from the object and stores them in the reference dictionary.
        """
        for key, value in item.iteritems():
            if isinstance(value, basestring) and value.startswith('&'):
                self._references[value[1:]] = getattr(obj, key)
            if isinstance(value, list):
                for i in value:
                    if isinstance(value, basestring) and i.startswith('&'):
                        self._references[value[1:]] = getattr(obj, value[1:])

    def _check_types(self, klass, obj):
        if not self.check_types:
            return obj
        else:
            mapper = class_mapper(klass)
            for table in mapper.tables:
                for key in obj.keys():
                    col = table.columns.get(key, None)
                    value = obj[key]
                    if value is not None and col is not None and col.type is not None:
                        for type_, func in self.default_casts.iteritems():
                            if isinstance(col.type, type_):
                                obj[key] = func(value)
                                break

                    if value is None and col is not None and isinstance(col.type, (String, Unicode)):
                        obj[key] = ''

            return obj

    def get_klass(self, klass_name):
        klass = None
        for module in self.modules:
            try:
                klass = getattr(module, klass_name)
                break
            except AttributeError:
                pass

        if klass is None:
            raise AttributeError('Class %s from %s not found in any module' % (klass_name, self.source))
        return klass

    def add_klass_with_values(self, klass, values):
        """
        klass is a type, values is a dictionary. Returns a new object.
        """
        ref_name = None
        keys = values.keys()
        if len(keys) == 1 and keys[0].startswith('&') and isinstance(values[keys[0]], dict):
            ref_name = keys[0]
            values = values[ref_name]
        resolved_values = values.copy()
        for key, value in resolved_values.iteritems():
            resolved_values[key] = self.resolve_value(value)

        resolved_values = self._check_types(klass, resolved_values)
        obj = self.create_obj(klass, resolved_values)
        self.session.add(obj)
        if ref_name:
            self.add_reference(ref_name, obj)
        if self.has_references(values):
            self.session.flush()
            self.set_references(obj, values)
        return obj

    def add_klasses(self, klass, items):
        """
        Returns a list of the new objects. These objects are already in session, so you don't *need* to do anything with them.
        """
        objects = []
        for item in items:
            obj = self.add_klass_with_values(klass, item)
            objects.append(obj)

        return objects

    def from_list(self, session, data):
        """
        Extract data from a list of groups in the form:

        [
            { #start of the first grouping
              ObjectName:[ #start of objects of type ObjectName
                          {'attribute':'value', 'attribute':'value' ... more attributes},
                          {'attribute':'value', 'attribute':'value' ... more attributes},
                          ...
                          }
                          ]
              ObjectName: [ ... more attr dicts here ... ]
              [commit:None] #optionally commit at the end of this grouping
              [flush:None]  #optionally flush at the end of this grouping
            }, #end of first grouping
            { #start of the next grouping
              ...
            } #end of the next grouping
        ]

        Data can also be nested, for example; here are three different ways to do it. The following:

        --- Mountaineering Data Document
        - MountainRegion:
          - name: Appalacians
            coast: East
            climate: { '!Climate': { high: 85, low: 13, precipitation: '54 inches annually' } }
            ranges:
              - '!MountainRange': { name: Blue Ridge Mountains, peak: Mount Mitchell }
              - '!MountainRange': { name: Piedmont Plateau, peak: Piedmont Crescent Peak }
            valleys:
              '!ValleyArea': [ { name: Hudson River Crevasse }, { name: Susquehanna Valleyway } ]

          Is equivalent to this:

        --- Mountaineering Data Document
        - Climate:
            '&appal-climate': { high: 85, low: 13, precipitation: '54 inches annually' }
        - MountainRange: ['&blue-ridge': { name: Blue Ridge Mountains, peak: Mount Mitchell },
                          '&peidmont': { name: Piedmont Plateau, peak: Piedmont Crescent Peak }]
        - ValleyArea:
          - '&hudson':
              name: Hudson River Crevasse
          - '&susq':
              name: Susquehanna Valleyway
        - MountainRegion:
          - name: Appalacians
            coast: East
            climate: '*appal-climate'
            ranges: ['*blue-ridge', '*peidmont']
            valleys: ['*hudson', '*susq']

        However, the nested data is not and cannot be added to the list of references. It is anonymous in that sense.

        Careful! Here are some pitfalls:

        This would double list the valleys. Not good. Like saying "valleys: [['*hudson', '*susq']]"
            valleys:
              - '!ValleyArea': [ { name: Hudson River Crevasse }, { name: Susquehanna Valleyway } ]

        This is not valid:
            climate: '!Climate': { high: 85, low: 13, precipitation: '54 inches annually' }

        Also, literal tags, like !Climate (without quotes), do not work, and will generally break.
        """
        self.session = session
        klass = None
        item = None
        group = None
        skip_keys = ['flush', 'commit', 'clear']
        try:
            for group in data:
                for name, items in group.iteritems():
                    if name not in skip_keys:
                        klass = self.get_klass(name)
                        self.add_klasses(klass, items)

                if 'flush' in group:
                    session.flush()
                if 'commit' in group:
                    session.commit()
                if 'clear' in group:
                    self.clear()

        except AttributeError as e:
            if hasattr(item, 'iteritems'):
                missing_refs = [ (key, value) for key, value in item.iteritems() if isinstance(value, basestring) and value.startswith('*') ]
                self.log_error(e, data, klass, item)
                if missing_refs:
                    log.error('*' * 80)
                    log.error('It is very possible you are missing a reference, or require a "flush:" between blocks to store the references')
                    log.error('here is a list of references that were not accessible (key, value): %s' % missing_refs)
                    log.error('*' * 80)
            else:
                self.log_error(e, data, klass, item)

        self.session = None
        return

    def log_error(self, e, data, klass, item):
        log.error('error occured while loading yaml data with output:\n%s' % pformat(data))
        log.error('references:\n%s' % pformat(self._references))
        log.error('class: %s' % klass)
        log.error('item: %s' % item)
        import traceback
        log.error(traceback.format_exc(e))


class YamlLoader(Loader):

    def loadf(self, session, filename):
        """
        Load a yaml file by filename.
        """
        self.source = filename
        s = open(filename).read()
        return self.loads(session, s)

    def loads(self, session, s):
        """
        Load a yaml string into the database.
        """
        data = load(s)
        if data:
            return self.from_list(session, data)