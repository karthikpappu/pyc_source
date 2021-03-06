# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/flask_admin/model/filters.py
# Compiled at: 2016-06-26 14:14:34
import time, datetime
from flask_admin.babel import lazy_gettext

class BaseFilter(object):
    """
        Base filter class.
    """

    def __init__(self, name, options=None, data_type=None):
        """
            Constructor.

            :param name:
                Displayed name
            :param options:
                List of fixed options. If provided, will use drop down instead of textbox.
            :param data_type:
                Client-side widget type to use.
        """
        self.name = name
        self.options = options
        self.data_type = data_type

    def get_options(self, view):
        """
            Return list of predefined options.

            Override to customize behavior.

            :param view:
                Associated administrative view class.
        """
        options = self.options
        if options:
            if callable(options):
                options = options()
            return options
        return

    def validate(self, value):
        """
            Validate value.

            If value is valid, returns `True` and `False` otherwise.

            :param value:
                Value to validate
        """
        try:
            self.clean(value)
            return True
        except ValueError:
            return False

    def clean(self, value):
        """
            Parse value into python format. Occurs before .apply()

            :param value:
                Value to parse
        """
        return value

    def apply(self, query, value):
        """
            Apply search criteria to the query and return new query.

            :param query:
                Query
            :param value:
                Search criteria
        """
        raise NotImplementedError()

    def operation(self):
        """
            Return readable operation name.

            For example: u'equals'
        """
        raise NotImplementedError()

    def __unicode__(self):
        return self.name


class BaseBooleanFilter(BaseFilter):
    """
        Base boolean filter, uses fixed list of options.
    """

    def __init__(self, name, options=None, data_type=None):
        super(BaseBooleanFilter, self).__init__(name, (
         (
          '1', lazy_gettext('Yes')),
         (
          '0', lazy_gettext('No'))), data_type)

    def validate(self, value):
        return value in ('0', '1')


class BaseIntFilter(BaseFilter):
    """
        Base Int filter. Adds validation and changes value to python int.

        Avoid using int(float(value)) to also allow using decimals, because it
        causes precision issues with large numbers.
    """

    def clean(self, value):
        return int(value)


class BaseFloatFilter(BaseFilter):
    """
        Base Float filter. Adds validation and changes value to python float.
    """

    def clean(self, value):
        return float(value)


class BaseIntListFilter(BaseFilter):
    """
        Base Integer list filter. Adds validation for int "In List" filter.

        Avoid using int(float(value)) to also allow using decimals, because it
        causes precision issues with large numbers.
    """

    def clean(self, value):
        return [ int(v.strip()) for v in value.split(',') if v.strip() ]


class BaseFloatListFilter(BaseFilter):
    """
        Base Float list filter. Adds validation for float "In List" filter.
    """

    def clean(self, value):
        return [ float(v.strip()) for v in value.split(',') if v.strip() ]


class BaseDateFilter(BaseFilter):
    """
        Base Date filter. Uses client-side date picker control.
    """

    def __init__(self, name, options=None, data_type=None):
        super(BaseDateFilter, self).__init__(name, options, data_type='datepicker')

    def clean(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()


class BaseDateBetweenFilter(BaseFilter):
    """
        Base Date Between filter. Consolidates logic for validation and clean.
        Apply method is different for each back-end.
    """

    def clean(self, value):
        return [ datetime.datetime.strptime(range, '%Y-%m-%d').date() for range in value.split(' to ')
               ]

    def operation(self):
        return lazy_gettext('between')

    def validate(self, value):
        try:
            value = [ datetime.datetime.strptime(range, '%Y-%m-%d').date() for range in value.split(' to ')
                    ]
            if len(value) == 2 and value[0] <= value[1]:
                return True
            return False
        except ValueError:
            return False


class BaseDateTimeFilter(BaseFilter):
    """
        Base DateTime filter. Uses client-side date time picker control.
    """

    def __init__(self, name, options=None, data_type=None):
        super(BaseDateTimeFilter, self).__init__(name, options, data_type='datetimepicker')

    def clean(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')


class BaseDateTimeBetweenFilter(BaseFilter):
    """
        Base DateTime Between filter. Consolidates logic for validation and clean.
        Apply method is different for each back-end.
    """

    def clean(self, value):
        return [ datetime.datetime.strptime(range, '%Y-%m-%d %H:%M:%S') for range in value.split(' to ')
               ]

    def operation(self):
        return lazy_gettext('between')

    def validate(self, value):
        try:
            value = [ datetime.datetime.strptime(range, '%Y-%m-%d %H:%M:%S') for range in value.split(' to ')
                    ]
            if len(value) == 2 and value[0] <= value[1]:
                return True
            return False
        except ValueError:
            return False


class BaseTimeFilter(BaseFilter):
    """
        Base Time filter. Uses client-side time picker control.
    """

    def __init__(self, name, options=None, data_type=None):
        super(BaseTimeFilter, self).__init__(name, options, data_type='timepicker')

    def clean(self, value):
        timetuple = time.strptime(value, '%H:%M:%S')
        return datetime.time(timetuple.tm_hour, timetuple.tm_min, timetuple.tm_sec)


class BaseTimeBetweenFilter(BaseFilter):
    """
        Base Time Between filter. Consolidates logic for validation and clean.
        Apply method is different for each back-end.
    """

    def clean(self, value):
        timetuples = [ time.strptime(range, '%H:%M:%S') for range in value.split(' to ')
                     ]
        return [ datetime.time(timetuple.tm_hour, timetuple.tm_min, timetuple.tm_sec) for timetuple in timetuples
               ]

    def operation(self):
        return lazy_gettext('between')

    def validate(self, value):
        try:
            timetuples = [ time.strptime(range, '%H:%M:%S') for range in value.split(' to ')
                         ]
            if len(timetuples) == 2 and timetuples[0] <= timetuples[1]:
                return True
            return False
        except ValueError:
            raise
            return False


def convert(*args):
    """
        Decorator for field to filter conversion routine.

        See :mod:`flask_admin.contrib.sqla.filters` for usage example.
    """

    def _inner(func):
        func._converter_for = list(map(lambda x: x.lower(), args))
        return func

    return _inner


class BaseFilterConverter(object):
    """
        Base filter converter.

        Derive from this class to implement custom field to filter conversion
        logic.
    """

    def __init__(self):
        self.converters = dict()
        for p in dir(self):
            attr = getattr(self, p)
            if hasattr(attr, '_converter_for'):
                for p in attr._converter_for:
                    self.converters[p] = attr