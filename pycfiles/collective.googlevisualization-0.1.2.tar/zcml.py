# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/collective/googlesystemstorage/zcml.py
# Compiled at: 2010-03-24 19:39:07
__doc__ = '\nZCML gss namespace handling, see meta.zcml\n'
__author__ = 'federica'
__docformat__ = 'restructuredtext'
import logging
from zope.interface import Interface
from zope.configuration.fields import GlobalObject, Tokens, PythonIdentifier
from iw.fss import config
from collective.googlesystemstorage.GoogleSystemStorage import GoogleSystemStorage

class ITypeWithGSSDirective(Interface):
    """Schema for gss:typeWithGSS directive"""
    __module__ = __name__
    class_ = GlobalObject(title='Class', description='Dotted name of class of AT based content type using GSS', required=True)
    fields = Tokens(title='Fields', description='Field name or space(s) separated field names', value_type=PythonIdentifier(), required=True)


def typeWithGSS(_context, class_, fields):
    """Register our monkey patch"""
    _context.action(discriminator=(class_.__module__, class_.__name__), callable=patchATType, args=(class_, fields))


logger = logging.getLogger(config.PROJECTNAME)
LOG = logger.info

def patchATType(class_, fields):
    """Processing the type patch"""
    global patchedTypesRegistry
    for fieldname in fields:
        field = class_.schema[fieldname]
        former_storage = field.storage
        field.storage = GoogleSystemStorage()
        field.registerLayer('storage', field.storage)
        if patchedTypesRegistry.has_key(class_):
            patchedTypesRegistry[class_][fieldname] = former_storage
        else:
            patchedTypesRegistry[class_] = {fieldname: former_storage}
        LOG("Field '%s' of %s is stored in file system.", fieldname, class_.meta_type)


patchedTypesRegistry = {}