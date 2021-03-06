# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/logviewer/flask_validator/fields.py
# Compiled at: 2017-01-13 11:34:46
# Size of source mod 2**32: 6038 bytes
import datetime
from flask import json
from flask_validator.exceptions import ValidationError
from mongoengine import fields as db
__author__ = 'stas'

class BaseField:
    __doc__ = '\n    Base Field\n    '
    serializer = None

    @classmethod
    def from_mongoengine_field(cls, mongoEngineField):
        return cls()

    def __init__(self, required=False, blank=True, default=None, validators=None, read_only=False):
        """
        :param required: if True then field should strictly present in data (but may be null)
        :param blank: if False then field should not be null or empty ("" for strings and so on)
        :param default: Default value for this field.
        """
        self._required = required
        self._blank = blank
        self._validators = validators or []
        self._default = default
        self._read_only = read_only

    def run_validate(self, validator, value):
        """
        :type validator: flask_validator.serializer.BaseSerializer

        Should return value which will be passed in BaseValidator.cleaned_data
        """
        if self._read_only:
            raise ValueError("You can't run validation on read only field!")
        else:
            if value is None:
                if self._default is not None:
                    value = self._default
            if value is None:
                if self._required:
                    raise ValidationError('Field is required')
                else:
                    return value
            for customVal in self._validators:
                customVal(validator, value)

            if value:
                value = self.validate(validator, value)
        return value

    def to_python(self, value):
        """For passed from Model instance value this method should return plain python object
        which will be used
        later in serialization

        :param value: value from db object
        """
        raise NotImplementedError()

    def validate(self, validator, value):
        pass

    def get_value_from_model_object(self, doc, field):
        """returns value for fieldName field and document doc"""
        return getattr(doc, field)


class StringField(BaseField):

    def to_python(self, value):
        if value:
            return str(value)

    def __init__(self, choices=None, **k):
        self.choices = choices
        (super(StringField, self).__init__)(**k)

    def validate(self, validator, value):
        if self.choices:
            if value not in self.choices:
                raise ValidationError('Value should be one of {}, got {}'.format(self.choices, value))
        return value


class BooleanField(BaseField):

    def to_python(self, value):
        return value

    def validate(self, validator, value):
        if value not in (True, False):
            raise ValidationError('Boolean is required')
        return value


class IntegerField(BaseField):

    def to_python(self, value):
        return value


class URLField(BaseField):

    def to_python(self, value):
        return value


class DateTimeField(BaseField):

    def to_python(self, value):
        if value:
            return value.strftime(self._format)

    def __init__(self, format='%Y-%m-%d %H:%M:%S', **k):
        self._format = format
        (super(DateTimeField, self).__init__)(**k)

    def validate(self, validator, value):
        try:
            return datetime.datetime.strptime(value, self._format)
        except:
            raise ValidationError('Incorrect DateTime string for {} format'.format(self._format))


class MongoEngineIdField(BaseField):

    def to_python(self, value):
        return str(value.id)

    def __init__(self, documentCls, **k):
        self._documentCls = documentCls
        (super(MongoEngineIdField, self).__init__)(**k)

    def validate(self, validator, value):
        ids = {str(item.id):item for item in self._documentCls.objects.all()}
        if value not in ids:
            raise ValidationError('Incorrect id: {}'.format(value))
        return ids[value]


class MethodField(BaseField):

    def __init__(self, methodName):
        super(MethodField, self).__init__(read_only=True)
        self.methodName = methodName

    def get_value_from_model_object(self, doc, field):
        return getattr(self.serializer, self.methodName)(doc)

    def to_python(self, value):
        return value


class ForeignKeyField(BaseField):

    def __init__(self, document_fieldname=None):
        super(ForeignKeyField, self).__init__(read_only=True)
        self.document_fieldname = document_fieldname

    def get_value_from_model_object(self, doc, field):
        field = self.document_fieldname or field
        parts = field.split('__')
        out = doc
        for item in parts:
            outCls = out.__class__
            if out:
                out = getattr(out, item)
                try:
                    outField = getattr(outCls, item)
                except AttributeError:
                    outField = None

        if out and outField:
            from flask_validator.utils import mongoengine_model_meta
            return mongoengine_model_meta.FIELD_MAPPING[outField.__class__].from_mongoengine_field(outField).to_python(out)
        else:
            return out

    def to_python(self, value):
        if isinstance(value, db.Document):
            return str(value.id)
        else:
            return value


class ListField(BaseField):

    def to_python(self, value):
        embedded = EmbeddedField()
        return list(map(embedded.to_python, value))


class EmbeddedField(BaseField):

    def to_python(self, value):
        if value:
            if isinstance(value, db.EmbeddedDocument):
                return json.loads(value.to_json())
        return value


class DictField(BaseField):

    def to_python(self, value):
        if value:
            return dict(value)
        else:
            return value