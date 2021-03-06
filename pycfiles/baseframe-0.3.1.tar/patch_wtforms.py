# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jace/Dropbox/projects/hasgeek/baseframe/baseframe/forms/patch_wtforms.py
# Compiled at: 2015-02-24 01:44:16
"""
Patches WTForms to add additional functionality as required by Baseframe.
"""
__all__ = []
import wtforms

def add_flags(validator, flags):
    validator.field_flags = tuple(flags) + tuple(getattr(validator, 'field_flags', ()))


add_flags(wtforms.validators.EqualTo, ('not_solo', ))
original_field_init = None

def __field_init__(self, label=None, validators=None, filters=tuple(), description='', id=None, default=None, widget=None, _form=None, _name=None, _prefix='', _translations=None, _meta=None, widget_attrs=None, **kwargs):
    original_field_init(self, label, validators, filters=filters, description=description, id=id, default=default, widget=widget, _form=_form, _name=_name, _prefix=_prefix, _translations=_translations, _meta=_meta, **kwargs)
    self.widget_attrs = widget_attrs or {}


if wtforms.fields.Field.__init__ is not __field_init__:
    original_field_init = wtforms.fields.Field.__init__
    wtforms.fields.Field.__init__ = __field_init__