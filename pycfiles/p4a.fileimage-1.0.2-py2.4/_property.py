# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/fileimage/_property.py
# Compiled at: 2007-11-30 08:40:44
_marker = object()

class DictProperty(object):
    """Computed fields based on a named dict on the context object.
    
    To demonstrate, we first build a sample schema.
      
      >>> from zope import interface, schema
      >>> class IFoo(interface.Interface):
      ...     text = schema.TextLine(title=u'Some Text')
      
    Next we construct a class which implements the schema and uses our
    *DictProperty*.
      
      >>> class Foo(object):
      ...     interface.implements(IFoo)
      ...     text = DictProperty(IFoo['text'], 'somedict')
      
    Lets instantiate our test class and try setting/getting the value
    of the *DictProperty* field.
      
      >>> foo = Foo()
      >>> foo.text = u'abc'
      >>> foo.text
      u'abc'
  
    Now lets make sure the internal dict was properly updated.
      
      >>> foo.somedict['text']
      u'abc'
      
    The reverse should also work, try updating the internal dict and
    make sure the field was updated properly.
    
      >>> foo.somedict['text'] = u'updated foo'
      >>> foo.text
      u'updated foo'
      
    """
    __module__ = __name__

    def __init__(self, field, attrname, name=None):
        if name is None:
            name = field.__name__
        self.__field = field
        self.__attrname = attrname
        self.__name = name
        return

    def __get__(self, inst, _class):
        if inst is None:
            return self
        d = inst.__dict__.get(self.__attrname, None)
        if d is None:
            return
        value = d.get(self.__name, _marker)
        if value is _marker:
            field = self.__field.bind(inst)
            value = getattr(field, 'default', _marker)
            if value is _marker:
                raise AttributeError(self.__name)
        return value

    def __set__(self, inst, value):
        field = self.__field.bind(inst)
        field.validate(value)
        d = inst.__dict__.get(self.__attrname, None)
        if d is None:
            d = {}
        if field.readonly and d.has_key(self.__name):
            raise ValueError(self.__name, 'field is readonly')
        d[self.__name] = value
        inst.__dict__[self.__attrname] = d
        return

    def __getattr__(self, name):
        return getattr(self.__field, name)