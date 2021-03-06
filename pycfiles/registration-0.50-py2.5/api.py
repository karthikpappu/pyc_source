# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/registration/ormmanager/api.py
# Compiled at: 2008-07-04 10:34:30
import dispatch

def create(class_, **kw):
    """Returns a new class_ object created using the keyword arguments."""
    raise NotImplementedError


create = dispatch.generic()(create)

def retrieve(class_, **kw):
    """Returns a list of existing class_ objects using the keyword arguments.
    
    Should return an empty list if there are no matching objects.
    If no keywords are provided, should return all class_ objects."""
    raise NotImplementedError


retrieve = dispatch.generic()(retrieve)

def retrieve_one(class_, **kw):
    """Returns a single class_ object using the keyword arguments.
    
    Should return None if there is no matching object.
    Should raise a LookupError when more than one object
    matches."""
    raise NotImplementedError


retrieve_one = dispatch.generic()(retrieve_one)

def update(obj, **kw):
    """Update an object using the keyword arguments."""
    raise NotImplementedError


update = dispatch.generic()(update)

def delete(obj):
    """Remove an object from the database."""
    raise NotImplementedError


delete = dispatch.generic()(delete)

def count(class_, **kw):
    """Count the number of objects with the given keyword arguments."""
    raise NotImplementedError


count = dispatch.generic()(count)
__all__ = [
 create, retrieve, retrieve_one, update, delete, count]