# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/apibits/api_resource.py
# Compiled at: 2015-08-31 22:18:13
import alman

class ApiResource(object):
    subclasses = set()
    subclass_dict = dict()
    api_method = None
    client = None

    @classmethod
    def api_attribute_names(cls):
        return cls._api_attributes.keys()

    def api_attributes(self):
        ret = {}
        for attr in self.__class__.api_attribute_names():
            ret[attr] = getattr(self, attr)

        return ret

    def changed_api_attributes(self):
        return {}

    def clear_api_attributes(self):
        for attr in self.__class__.api_attribute_names():
            setattr(self, attr, None)

        return

    def determine_api_attribute_value(self, name, raw_value):
        if isinstance(self.__class__._api_attributes[name], dict) and 'constructor' in self.__class__._api_attributes[name].keys():
            klass = self.__class__._api_attributes[name]['constructor']
            return klass.construct(raw_value)
        else:
            return raw_value

    def get_client(self):
        if self.client == None:
            self.client = self.__class__.default_client()
        return self.client

    @classmethod
    def api_subclasses(cls):
        return cls.subclasses

    @classmethod
    def api_subclass(cls, name):
        if name in cls.subclass_dict.keys():
            return cls.subclass_dict[name]

    @classmethod
    def register_api_subclass(cls, subclass, name=None):
        cls.subclasses.add(cls)
        key = name or subclass.__name__
        cls.subclass_dict[key] = subclass

    @classmethod
    def default_client(cls):
        return alman.default_client()

    @classmethod
    def construct(cls, json={}, api_method=None):
        return cls().refresh_from(json, api_method)

    def refresh_from(self, json={}, api_method=None, client=None):
        if not isinstance(json, dict):
            json = {'id': json}
        self.clear_api_attributes()
        self.api_method = api_method
        self.json = json
        self.client = client
        for key, value in self.json.items():
            if key in self.__class__.api_attribute_names():
                setattr(self, key, self.determine_api_attribute_value(key, value))

        return self

    def __init__(self, json=None, api_method=None, client=None):
        self.refresh_from(json, api_method, client)

    _api_attributes = {}