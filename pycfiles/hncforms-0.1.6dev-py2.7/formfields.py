# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\hncforms\formfields.py
# Compiled at: 2013-05-23 14:42:20
from datetime import datetime
from operator import methodcaller
import formencode
from formencode.validators import OneOf
from hncforms.validators import TypeAheadValidator, DateValidator
from pyramid.renderers import render
import simplejson

class NullConfigModel(object):
    name = None

    def getKey(self, request):
        return ''

    def getLabel(self, request):
        return '---'


class HtmlAttrs(object):
    classes = ''

    def __init__(self, required=False, important=False, placeholder='', **attrs):
        self.required = required
        self.important = important
        self.attrs = attrs
        if placeholder:
            self.attrs['placeholder'] = placeholder

    def getClasses(self):
        classes = self.classes
        if self.required:
            classes += ' required'
        if self.important:
            classes += ' important'
        return classes

    def getInputAttrs(self, request):
        _ = request._
        return (' ').join([ ('{}="{}"').format(k.replace('_', '-'), _(v)) for k, v in self.attrs.items() ])

    def getGroupAttrs(self):
        return ''

    def getGroupClasses(self):
        return ''


NONE = HtmlAttrs()
REQUIRED = HtmlAttrs(True)
IMPORTANT = HtmlAttrs(False, True)

class Placeholder(HtmlAttrs):

    def __init__(self, placeholder='', required=False, important=False, **attrs):
        self.placeholder = placeholder
        self.required = required
        self.important = important
        self.attrs = attrs
        self.attrs['placeholder'] = placeholder


class DependentAttrs(HtmlAttrs):

    def __init__(self, placeholder, dependency, dependencyValue, required=False, important=False, **attrs):
        self.required = required
        self.important = important
        self.dependency = dependency
        self.dependencyValue = dependencyValue
        self.attrs = attrs
        self.attrs['placeholder'] = placeholder

    def getGroupClasses(self):
        return 'dependent-control'

    def getGroupAttrs(self):
        return ('data-dependency="{}" data-dependency-value="{}"').format(self.dependency, self.dependencyValue)


class PictureUploadAttrs(HtmlAttrs):

    def __init__(self, singleFile=True, types='jpg,gif,png', required=False, important=False, **attrs):
        self.singleFile = singleFile
        self.types = types
        self.required = required
        self.important = important
        self.attrs = attrs

    def getClasses(self):
        return ''

    def getGroupClasses(self):
        return 'file-upload-control'

    def getGroupAttrs(self):
        return ('data-upload-single="{}" data-file-types="{}"').format(self.singleFile, self.types)


class BaseSchema(formencode.Schema):
    filter_extra_fields = False
    allow_extra_fields = True


class BaseForm(object):
    id = 'formdata'
    classes = 'form-validated'
    fields = []
    extra_forms = []
    pre_validators = []
    chained_validators = []
    template = 'hncforms:templates/baseform.html'

    def render(self, request):
        return render(self.template, {'form': self}, request)

    @classmethod
    def getSchema(cls, request, values):
        validators = {}
        for v in cls.fields:
            if v.is_validated:
                validators.update(v.getValidator(request))

        for form in cls.extra_forms:
            validators[form.id] = form.getSchema(request)

        validators['pre_validators'] = cls.pre_validators
        validators['chained_validators'] = cls.chained_validators
        return BaseSchema(**validators)


class BaseField(object):
    is_validated = False
    html_help = None
    group_classes = ''
    label_classes = ''
    control_classes = ''
    input_classes = ''
    attrs = NONE


class HeadingField(BaseField):
    tag = 'legend'
    template = 'hncforms:templates/heading.html'

    def __init__(self, format_string, classes=''):
        self.format_string = format_string
        self.classes = classes

    def getHeading(self, request, view):
        return unicode(self.format_string).format(request=request, view=view)

    def render(self, prefix, request, values, errors, view=None):
        return render(self.template, {'widget': self, 'view': view}, request)

    def getClasses(self):
        return self.classes


class PlainHeadingField(BaseField):

    def __init__(self, label, tag='h4', classes=''):
        self.label = label
        self.tag = tag
        self.classes = classes

    def render(self, prefix, request, values, errors, view=None):
        return ('<{0.tag} class="{0.classes}">{1}</{0.tag}>').format(self, request._(self.label))


class Field(BaseField):
    template = 'hncforms:templates/basefield.html'
    is_validated = True
    validator_args = {}
    if_empty = ''
    min = None
    max = None
    type = 'text'
    input_classes = ''

    def __init__(self, name, label, attrs=NONE, classes='', validator_args={}, group_classes='', label_classes='', input_classes='', **kwargs):
        self.name = name
        self.label = label
        self.attrs = attrs
        self.validator_args = validator_args or self.validator_args
        self.group_classes = group_classes or self.group_classes
        self.label_classes = label_classes
        self.input_classes = input_classes or self.input_classes
        self.input_classes = ('{} {}').format(self.input_classes, classes)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def getInputAttrs(self, request):
        attrs = self.attrs.getInputAttrs(request)
        if self.min:
            attrs += (' minlength="{}"').format(self.min)
        if self.max:
            attrs += (' maxlength="{}"').format(self.max)
        return attrs

    def getValidatorArgs(self):
        params = self.validator_args.copy()
        if self.validator_args:
            params.update(self.validator_args)
        params['required'] = self.attrs.required
        params['not_empty'] = self.attrs.required
        if self.min:
            params['min'] = self.min
        if self.max:
            params['max'] = self.max
        if not self.attrs.required:
            params.setdefault('if_missing', None)
        return params

    def getValidator(self, request):
        return {self.name: self._validator(**self.getValidatorArgs())}

    def valueToForm(self, value):
        if value is None:
            return ''
        else:
            return value

    def hasLabel(self):
        return bool(self.label)

    def getLabel(self, request):
        return request._(self.label)

    def getName(self, prefix):
        return ('{}.{}').format(prefix, self.name)

    def getClasses(self):
        return ('{} {}').format(self.input_classes, self.attrs.getClasses())

    def getValues(self, name, request, values, errors, view):
        return {'value': values.get(name, self.if_empty), 'error': errors.get(name, self.if_empty)}

    def render(self, prefix, request, values, errors, view=None):
        if isinstance(errors, formencode.Invalid):
            errors = errors.error_dict
        params = self.getValues(self.name, request, values, errors, view)
        params.update({'widget': self, 'prefix': prefix, 'view': view})
        return render(self.template, params, request)

    def renderControl(self, prefix, request, values, errors, view=None):
        if isinstance(errors, formencode.Invalid):
            errors = errors.error_dict
        params = self.getValues(self.name, request, values, errors, view)
        params.update({'widget': self, 'prefix': prefix, 'view': view})
        t = self.template.replace('.html', '#controls.html')
        return render(t, params, request)


class MultipleFormField(Field):
    template = 'hncforms:templates/repeatableform.html'
    fields = []
    add_more_link_label = '+'

    def __init__(self, name, label=None, attrs=NONE, classes='form-embedded-wrapper'):
        self.name = name
        self.label = label
        self.attrs = attrs
        self.classes = classes

    def getClasses(self):
        return self.classes

    def getValidator(self, request):
        validators = {}
        for v in self.fields:
            if v.is_validated:
                validators.update(v.getValidator(request))

        return {self.name: formencode.ForEach(BaseSchema(**validators), not_empty=self.attrs.required)}

    def render(self, prefix, request, values, errors, view=None):
        name = self.name
        return render(self.template, {'widget': self, 'prefix': ('{}.{}').format(prefix, self.name), 'value': values.get(name, ''), 'error': errors.get(name, ''), 'view': view}, request)


class StaticHiddenField(Field):
    _validator = formencode.validators.String

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, prefix, request, values, errors, view=None):
        return ('<input type="hidden" name="{}" value="{}"/>').format(self.getName(prefix), self.value)


class HiddenField(Field):
    _validator = formencode.validators.String

    def render(self, prefix, request, values, errors, view=None):
        return ('<input type="hidden" name="{}" value="{}"/>').format(self.getName(prefix), values.get(self.name, ''))

    def __init__(self, name):
        self.name = name


class StringField(Field):
    _validator = formencode.validators.String


class TextareaField(Field):
    template = 'hncforms:templates/textarea.html'
    _validator = formencode.validators.String


class IntField(Field):
    input_classes = 'digits'
    _validator = formencode.validators.Int
    maxlength = 6

    def getInputAttrs(self, request):
        attrs = self.attrs.getInputAttrs(request)
        if self.min:
            attrs += (' min="{}"').format(self.min)
        if self.max:
            attrs += (' max="{}"').format(self.max)
        if self.maxlength:
            attrs += (' maxlength="{}"').format(self.maxlength)
        return attrs


class URLField(Field):
    input_classes = 'input-xxlarge'
    _validator = formencode.validators.String


class EmailField(StringField):
    input_classes = ' email'
    type = 'email'
    validator_args = {'resolve_domain': True}
    _validator = formencode.validators.Email


class PasswordField(StringField):
    input_classes = ''
    type = 'password'
    validator_args = {'min': 6}
    _validator = formencode.validators.String


class CheckboxField(Field):
    template = 'hncforms:templates/checkbox.html'
    input_classes = 'checkbox'
    value = 'true'
    validator_args = {'if_missing': False}
    _validator = formencode.validators.StringBool


class CheckboxPostField(CheckboxField):
    template = 'hncforms:templates/checkbox_post.html'
    input_classes = ''


class RadioBoolField(CheckboxField):
    template = 'hncforms:templates/radiobool.html'
    input_classes = 'radio'


class DateField(StringField):
    input_classes = ' date-field'
    format = '%Y-%m-%d'

    def __init__(self, name, label, attrs=NONE, validator_args={}, input_classes='', group_classes=''):
        self.name = name
        self.label = label
        self.attrs = attrs
        self.validator_args = validator_args
        self.input_classes = input_classes
        self.group_classes = group_classes

    def valueToForm(self, value):
        if not value:
            return ''
        else:
            if isinstance(value, basestring):
                return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S').strftime(self.format)
            return value.strftime(self.format)

    def getValidator(self, request):
        return {self.name: DateValidator(format=self.format, not_empty=self.attrs.required)}


class ChoiceField(Field):
    template = 'hncforms:templates/dropdown.html'

    def __init__(self, name, label, optionGetter, attrs=NONE, input_classes='', group_classes=''):
        self.name = name
        self.label = label
        self.attrs = attrs
        self.input_classes = input_classes
        self.group_classes = group_classes
        self.optionGetter = optionGetter

    def getValidator(self, request):
        return {self.name: OneOf(map(methodcaller('getKey', request), self.optionGetter(request)), hideList=True)}

    def getOptions(self, request):
        return self.optionGetter(request)

    def isSelected(self, option, value, request):
        return option.getKey(request) == value


class RadioChoice(ChoiceField):
    template = 'hncforms:templates/radioselect.html'
    input_classes = 'radio inline'


def configattr(name, default_none):

    def f(request):
        values = getattr(request.context.config, name)
        if default_none:
            values = [
             NullConfigModel()] + list(values)
        return values

    return f


class ConfigChoiceField(ChoiceField):

    def __init__(self, name, label, configAttr, attrs=NONE, default_none=True, input_classes=''):
        self.name = name
        self.label = label
        self.attrs = attrs
        self.input_classes = input_classes
        self.optionGetter = configattr(configAttr, default_none)


class TypeAheadField(StringField):
    template = 'hncforms:templates/typeahead.html'
    if_empty = ''

    def __init__(self, name, label, api_url, api_result, dependency=None, attrs=NONE, classes='typeahead', validator_args={}):
        super(TypeAheadField, self).__init__(name, label, attrs, classes, validator_args)
        self.dependency = dependency
        self.api_result = api_result
        self.api_type = None
        self.api_url = api_url
        return


class ConfigTypeAheadField(StringField):
    template = 'hncforms:templates/typeahead_config.html'
    if_empty = ''

    def __init__(self, name, label, configAttr, attrs=NONE, classes='configtypeahead'):
        super(ConfigTypeAheadField, self).__init__(name, label, attrs, classes)
        self.configAttr = configAttr


class TagSearchField(StringField):
    template = 'hncforms:templates/tagsearch.html'

    def __init__(self, name, label, api_url, api_result, api_allow_new=True, query_extra={}, attrs=NONE, classes='tagsearch', group_classes='', label_classes='', input_classes=''):
        super(TagSearchField, self).__init__(name, label, attrs, classes, group_classes=group_classes, label_classes=label_classes, input_classes=input_classes)
        self.api_result = api_result
        self.api_allow_new = 'true' if api_allow_new else 'false'
        self.api_type = None
        self.api_url = api_url
        if query_extra:
            self.query_extra = simplejson.dumps(query_extra).replace('"', '&quot;')
        else:
            self.query_extra = None
        return

    def getValidator(self, request):
        return {self.name: formencode.ForEach(name=formencode.validators.String(required=True))}

    def getValueData(self, name, request, value):
        if value:
            return simplejson.dumps(value)
        return 'null'

    def getQueryExtra(self):
        if self.query_extra:
            return ('data-query-extra="{}"').format(self.query_extra)
        else:
            return ''


class TokenTypeAheadField(StringField):
    template = 'hncforms:templates/typeahead_token.html'

    def __init__(self, name, label, api_url, api_result, dependency=None, attrs=NONE, classes='typeahead', validator_args={}):
        super(TokenTypeAheadField, self).__init__(name, label, attrs, classes, validator_args)
        self.dependency = dependency
        self.api_result = api_result
        self.api_url = api_url

    def getValidator(self, request):
        return {self.name: TypeAheadValidator(self.attrs)}

    def getValues(self, name, request, values, errors, view):
        return {'value': values.get(name, {}), 'error': errors.get(name, {})}


def MultiConfigChoiceField(name, label, configKey, *args, **kwargs):

    class cls(MultipleFormField):
        fields = [
         ConfigChoiceField(name, label, configKey)]

    return cls(*args, **kwargs)


class CombinedField(StringField):
    template = 'hncforms:templates/combined.html'

    def __init__(self, fields, label, *args, **kwargs):
        super(StringField, self).__init__(None, label, *args, **kwargs)
        self.fields = fields
        return

    def getValidator(self, request):
        validator = {}
        for w in self.fields:
            validator.update(w.getValidator(request))

        return validator

    def getValues(self, name, request, values, errors, view):
        return {'value': values, 'error': {f.name:errors.get(f.name) for f in self.fields if errors.get(f.name)}}