# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/validators.py
# Compiled at: 2016-04-19 08:18:59
# Size of source mod 2**32: 13423 bytes
from api_star.compat import string_types
from api_star.exceptions import ValidationError
from api_star.utils import parse_iso8601_date, parse_iso8601_time, parse_iso8601_datetime
import datetime, decimal
errors = {'null': 'May not be null.', 
 'blank': 'May not be blank.', 
 'empty': 'May not be empty.', 
 'too_large': 'Input too large.', 
 'required': 'This field is required.', 
 'type': 'Not a valid {type_name} type.', 
 'value': 'Not a valid {type_name} value.', 
 'max_value': 'Value must not be greater than {max_value}.', 
 'min_value': 'Value must not be less than {min_value}.', 
 'max_length': 'Length must not be greater than {max_length}.', 
 'min_length': 'Length must not be less than {min_length}.', 
 'index': 'Invalid item at index {index}.'}

class ignore(object):
    __doc__ = '\n    A sentinal value used to indicate an optional field with no default value.\n    '


def optional(validator, default=ignore):
    """
    For use with `object_of(...)` to indicate optional fields.
    """
    validator.default_value = default
    return validator


def is_null(value, allow_null):
    if value not in ('', None):
        return False
    if not allow_null:
        if value is None:
            raise ValidationError(errors['null'])
        raise ValidationError(errors['blank'])
    return True


def is_blank(value, allow_blank):
    if value not in ('', None):
        return False
    if value is None:
        raise ValidationError(errors['null'])
    if not allow_blank:
        raise ValidationError(errors['blank'])
    return True


def boolean(allow_blank=True):
    valid_types = string_types + (int, bool)
    true_values = ('true', '1', 't', True, 1)
    false_values = ('false', '0', 'f', False, 0)

    def validator(value):
        if is_blank(value, allow_blank):
            return False
        if not isinstance(value, valid_types):
            raise ValidationError(errors['type'].format(type_name='boolean'))
        if isinstance(value, string_types):
            value = value.lower()
        if value in true_values:
            return True
        if value in false_values:
            return False
        raise ValidationError(errors['value'].format(type_name='boolean'))

    return validator


def nullable_boolean():
    boolean_validator = boolean()

    def validator(value):
        if value in ('', None):
            return
        return boolean_validator(value)

    return validator


def text(max_length=None, min_length=None, trim_whitespace=True, allow_blank=False):
    """
    Validates a string.
    By default the input will be cleaned by removing leading and trailing whitespace.
    """

    def validator(value):
        if value is None:
            raise ValidationError(errors['null'])
        if not isinstance(value, string_types):
            raise ValidationError(errors['type'].format(type_name='string'))
        if trim_whitespace:
            value = value.strip()
        if is_blank(value, allow_blank):
            return ''
        if max_length is not None:
            if len(value) > max_length:
                raise ValidationError(errors['max_length'].format(max_length=max_length))
        if min_length is not None:
            if len(value) < min_length:
                raise ValidationError(errors['min_length'].format(min_length=min_length))
        return value

    return validator


def email(trim_whitespace=True, allow_blank=False):
    """
    Validates an email string.
    """
    base_validator = text(max_length=254, trim_whitespace=trim_whitespace, allow_blank=allow_blank)

    def validator(value):
        value = base_validator(value)
        if '@' not in value:
            raise ValidationError(errors['value'].format(type_name='email'))
        return value

    return validator


def url(trim_whitespace=True, allow_blank=False):
    """
    Validates a URL string.
    """
    base_validator = text(max_length=2000, trim_whitespace=trim_whitespace, allow_blank=allow_blank)

    def validator(value):
        value = base_validator(value)
        if ':' not in value:
            raise ValidationError(errors['value'].format(type_name='url'))
        return value

    return validator


def integer(max_value=None, min_value=None, allow_null=False):
    """
    Validates an integer.
    """

    def validator(value):
        if is_null(value, allow_null):
            return
        if isinstance(value, string_types):
            if len(value) > 100:
                raise ValidationError(errors['too_large'])
        try:
            value = int(value)
        except TypeError:
            raise ValidationError(errors['type'].format(type_name='integer'))
        except ValueError:
            raise ValidationError(errors['value'].format(type_name='integer'))

        if max_value is not None:
            if value > max_value:
                raise ValidationError(errors['max_value'].format(max_value=max_value))
        if min_value is not None:
            if value < min_value:
                raise ValidationError(errors['min_value'].format(min_value=min_value))
        return value

    return validator


def number(max_value=None, min_value=None, allow_null=False):
    """
    Validates a floating point numer.
    """

    def validator(value):
        if is_null(value, allow_null):
            return
        if isinstance(value, string_types):
            if len(value) > 100:
                raise ValidationError(errors['too_large'])
        try:
            value = float(value)
        except TypeError:
            raise ValidationError(errors['type'].format(type_name='number'))
        except ValueError:
            raise ValidationError(errors['value'].format(type_name='number'))

        if max_value is not None:
            if value > max_value:
                raise ValidationError(errors['max_value'].format(max_value=max_value))
        if min_value is not None:
            if value < min_value:
                raise ValidationError(errors['min_value'].format(min_value=min_value))
        return value

    return validator


def fixed_precision(minor_digits=None, major_digits=None, max_value=None, min_value=None, allow_null=False):
    """
    Validates a decimal with fixed range of precision. For example:

    fixed_precision(minor_digits=2, major_digits=6)

    The above will return decimal values with 0.01 precision, up to
    a maximum value of 999,999.99, or a minimum value of -999,999.99.
    """
    if minor_digits is not None:
        quantizer = decimal.Decimal('10') ** (-minor_digits)
    else:
        quantizer = None
    if major_digits is not None:
        if max_value is None:
            max_value = decimal.Decimal('10') ** major_digits - 1
            if quantizer is not None:
                max_value += decimal.Decimal('1') - quantizer

    def validator(value):
        if is_null(value, allow_null):
            return
        if isinstance(value, string_types):
            if len(value) > 100:
                raise ValidationError(errors['too_large'])
        try:
            value = decimal.Decimal(value)
        except (ValueError, decimal.InvalidOperation):
            raise ValidationError(errors['value'].format(type_name='number'))
        except TypeError:
            raise ValidationError(errors['type'].format(type_name='number'))

        if quantizer is not None:
            value = value.quantize(quantizer, rounding=decimal.ROUND_HALF_UP)
        if max_value is not None:
            if value > max_value:
                raise ValidationError(errors['max_value'].format(max_value=max_value))
        if min_value is not None:
            if value < min_value:
                raise ValidationError(errors['min_value'].format(min_value=min_value))
        return value

    return validator


def iso_date(allow_null=False):
    """
    Validates an ISO-8601 formatted date.
    """

    def validator(value):
        if is_null(value, allow_null):
            return
        if isinstance(value, datetime.datetime):
            raise ValidationError(errors['type'].format(type_name='date'))
        if isinstance(value, datetime.date):
            return value
        if not isinstance(value, string_types):
            raise ValidationError(errors['type'].format(type_name='date'))
        if len(value) > 100:
            raise ValidationError(errors['too_large'])
        try:
            return parse_iso8601_date(value)
        except ValueError:
            raise ValidationError(errors['value'].format(type_name='date'))

    return validator


def iso_time(allow_null=False):
    """
    Validates an ISO-8601 formatted time.
    """

    def validator(value):
        if is_null(value, allow_null):
            return
        if isinstance(value, datetime.time):
            return value
        if not isinstance(value, string_types):
            raise ValidationError(errors['type'].format(type_name='time'))
        if len(value) > 100:
            raise ValidationError(errors['too_large'])
        try:
            return parse_iso8601_time(value)
        except ValueError:
            raise ValidationError(errors['value'].format(type_name='time'))

    return validator


def iso_datetime(allow_null=False, default_timezone=None):
    """
    Validates an ISO-8601 formatted datetime.
    """

    def validator(value):
        if is_null(value, allow_null):
            return
        if isinstance(value, datetime.datetime):
            return value
        if not isinstance(value, string_types):
            raise ValidationError(errors['type'].format(type_name='datetime'))
        if len(value) > 100:
            raise ValidationError(errors['too_large'])
        try:
            return parse_iso8601_datetime(value, default_timezone=default_timezone)
        except ValueError:
            raise ValidationError(errors['value'].format(type_name='datetime'))

    return validator


def choice(options):
    pass


def multiple_choice(options):
    pass


def list_of(child_validator, allow_empty=True):
    """
    Validates a list of items. For example:

    list_of(integer())

    The above will validate values like `[123, 456, 789]`.
    By default, empty lists are treated as valid.
    """

    def validator(value):
        if not isinstance(value, list):
            raise ValidationError(errors['type'].format(type_name='list'))
        if not allow_empty:
            if not value:
                raise ValidationError(errors['empty'])
        validated = []
        for idx, item in enumerate(value):
            try:
                validated.append(child_validator(item))
            except ValidationError as exc:
                index_msg = errors['index'].format(index=idx)
                raise ValidationError(index_msg + ' ' + exc.description)

        return validated

    return validator


def mapping_of(child_validator, allow_empty=True):
    """
    Validates a mapping of strings to items. For example:

    mapping_of(integer())

    The above will validate values like `{'tom': 123, 'sue': 456}`.
    By default, empty mappings are treated as valid.
    """

    def validator(value):
        if not isinstance(value, dict):
            raise ValidationError(errors['type'].format(type_name='object'))
        if not allow_empty:
            if not value:
                raise ValidationError(errors['empty'])
        validated = {}
        invalid = {}
        for key, item in value.items():
            try:
                validated[key] = child_validator(item)
            except ValidationError as exc:
                invalid[key] = exc.description

        if invalid:
            raise ValidationError(invalid)
        return validated

    return validator


def object_of(spec):
    """
    Validates a mapping of a fixed set of fields. For example:

    object_of({
        'title': text(max_length=100),
        'date': iso_date(),
        'tags': list_of(text(max_length=20))
    })

    Use the `optional()` function for fields that may be omitted.

    object_of({
        'title': text(max_length=100),
        'date': optional(iso_date()),
        'tags': optional(list_of(text(max_length=20)), default=[])
    })
    """

    def validator(value):
        if not isinstance(value, dict):
            raise ValidationError(errors['type'].format(type_name='object'))
        validated = {}
        invalid = {}
        for key, validator in spec.items():
            try:
                item = value[key]
            except KeyError:
                try:
                    item = validator.default_value
                except AttributeError:
                    invalid[key] = errors['required']
                else:
                    if item is not ignore:
                        validated[key] = item
            else:
                try:
                    validated[key] = validator(item)
                except ValidationError as exc:
                    invalid[key] = exc.description

        if invalid:
            raise ValidationError(invalid)
        return validated

    return validator