# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/views/generic/dates.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
import datetime
from django.conf import settings
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.views.generic.base import View
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin

class YearMixin(object):
    """
    Mixin for views manipulating year-based data.
    """
    year_format = b'%Y'
    year = None

    def get_year_format(self):
        """
        Get a year format string in strptime syntax to be used to parse the
        year from url variables.
        """
        return self.year_format

    def get_year(self):
        """
        Return the year for which this view should display data.
        """
        year = self.year
        if year is None:
            try:
                year = self.kwargs[b'year']
            except KeyError:
                try:
                    year = self.request.GET[b'year']
                except KeyError:
                    raise Http404(_(b'No year specified'))

        return year

    def get_next_year(self, date):
        """
        Get the next valid year.
        """
        return _get_next_prev(self, date, is_previous=False, period=b'year')

    def get_previous_year(self, date):
        """
        Get the previous valid year.
        """
        return _get_next_prev(self, date, is_previous=True, period=b'year')

    def _get_next_year(self, date):
        """
        Return the start date of the next interval.

        The interval is defined by start date <= item date < next start date.
        """
        return date.replace(year=date.year + 1, month=1, day=1)

    def _get_current_year(self, date):
        """
        Return the start date of the current interval.
        """
        return date.replace(month=1, day=1)


class MonthMixin(object):
    """
    Mixin for views manipulating month-based data.
    """
    month_format = b'%b'
    month = None

    def get_month_format(self):
        """
        Get a month format string in strptime syntax to be used to parse the
        month from url variables.
        """
        return self.month_format

    def get_month(self):
        """
        Return the month for which this view should display data.
        """
        month = self.month
        if month is None:
            try:
                month = self.kwargs[b'month']
            except KeyError:
                try:
                    month = self.request.GET[b'month']
                except KeyError:
                    raise Http404(_(b'No month specified'))

        return month

    def get_next_month(self, date):
        """
        Get the next valid month.
        """
        return _get_next_prev(self, date, is_previous=False, period=b'month')

    def get_previous_month(self, date):
        """
        Get the previous valid month.
        """
        return _get_next_prev(self, date, is_previous=True, period=b'month')

    def _get_next_month(self, date):
        """
        Return the start date of the next interval.

        The interval is defined by start date <= item date < next start date.
        """
        if date.month == 12:
            return date.replace(year=date.year + 1, month=1, day=1)
        else:
            return date.replace(month=date.month + 1, day=1)

    def _get_current_month(self, date):
        """
        Return the start date of the previous interval.
        """
        return date.replace(day=1)


class DayMixin(object):
    """
    Mixin for views manipulating day-based data.
    """
    day_format = b'%d'
    day = None

    def get_day_format(self):
        """
        Get a day format string in strptime syntax to be used to parse the day
        from url variables.
        """
        return self.day_format

    def get_day(self):
        """
        Return the day for which this view should display data.
        """
        day = self.day
        if day is None:
            try:
                day = self.kwargs[b'day']
            except KeyError:
                try:
                    day = self.request.GET[b'day']
                except KeyError:
                    raise Http404(_(b'No day specified'))

        return day

    def get_next_day(self, date):
        """
        Get the next valid day.
        """
        return _get_next_prev(self, date, is_previous=False, period=b'day')

    def get_previous_day(self, date):
        """
        Get the previous valid day.
        """
        return _get_next_prev(self, date, is_previous=True, period=b'day')

    def _get_next_day(self, date):
        """
        Return the start date of the next interval.

        The interval is defined by start date <= item date < next start date.
        """
        return date + datetime.timedelta(days=1)

    def _get_current_day(self, date):
        """
        Return the start date of the current interval.
        """
        return date


class WeekMixin(object):
    """
    Mixin for views manipulating week-based data.
    """
    week_format = b'%U'
    week = None

    def get_week_format(self):
        """
        Get a week format string in strptime syntax to be used to parse the
        week from url variables.
        """
        return self.week_format

    def get_week(self):
        """
        Return the week for which this view should display data
        """
        week = self.week
        if week is None:
            try:
                week = self.kwargs[b'week']
            except KeyError:
                try:
                    week = self.request.GET[b'week']
                except KeyError:
                    raise Http404(_(b'No week specified'))

        return week

    def get_next_week(self, date):
        """
        Get the next valid week.
        """
        return _get_next_prev(self, date, is_previous=False, period=b'week')

    def get_previous_week(self, date):
        """
        Get the previous valid week.
        """
        return _get_next_prev(self, date, is_previous=True, period=b'week')

    def _get_next_week(self, date):
        """
        Return the start date of the next interval.

        The interval is defined by start date <= item date < next start date.
        """
        return date + datetime.timedelta(days=7 - self._get_weekday(date))

    def _get_current_week(self, date):
        """
        Return the start date of the current interval.
        """
        return date - datetime.timedelta(self._get_weekday(date))

    def _get_weekday(self, date):
        """
        Return the weekday for a given date.

        The first day according to the week format is 0 and the last day is 6.
        """
        week_format = self.get_week_format()
        if week_format == b'%W':
            return date.weekday()
        if week_format == b'%U':
            return (date.weekday() + 1) % 7
        raise ValueError(b'unknown week format: %s' % week_format)


class DateMixin(object):
    """
    Mixin class for views manipulating date-based data.
    """
    date_field = None
    allow_future = False

    def get_date_field(self):
        """
        Get the name of the date field to be used to filter by.
        """
        if self.date_field is None:
            raise ImproperlyConfigured(b'%s.date_field is required.' % self.__class__.__name__)
        return self.date_field

    def get_allow_future(self):
        """
        Returns `True` if the view should be allowed to display objects from
        the future.
        """
        return self.allow_future

    @cached_property
    def uses_datetime_field(self):
        """
        Return `True` if the date field is a `DateTimeField` and `False`
        if it's a `DateField`.
        """
        model = self.get_queryset().model if self.model is None else self.model
        field = model._meta.get_field(self.get_date_field())
        return isinstance(field, models.DateTimeField)

    def _make_date_lookup_arg(self, value):
        """
        Convert a date into a datetime when the date field is a DateTimeField.

        When time zone support is enabled, `date` is assumed to be in the
        current time zone, so that displayed items are consistent with the URL.
        """
        if self.uses_datetime_field:
            value = datetime.datetime.combine(value, datetime.time.min)
            if settings.USE_TZ:
                value = timezone.make_aware(value, timezone.get_current_timezone())
        return value

    def _make_single_date_lookup(self, date):
        """
        Get the lookup kwargs for filtering on a single date.

        If the date field is a DateTimeField, we can't just filter on
        date_field=date because that doesn't take the time into account.
        """
        date_field = self.get_date_field()
        if self.uses_datetime_field:
            since = self._make_date_lookup_arg(date)
            until = self._make_date_lookup_arg(date + datetime.timedelta(days=1))
            return {b'%s__gte' % date_field: since, 
               b'%s__lt' % date_field: until}
        else:
            return {date_field: date}


class BaseDateListView(MultipleObjectMixin, DateMixin, View):
    """
    Abstract base class for date-based views displaying a list of objects.
    """
    allow_empty = False
    date_list_period = b'year'

    def get(self, request, *args, **kwargs):
        self.date_list, self.object_list, extra_context = self.get_dated_items()
        context = self.get_context_data(object_list=self.object_list, date_list=self.date_list)
        context.update(extra_context)
        return self.render_to_response(context)

    def get_dated_items(self):
        """
        Obtain the list of dates and items.
        """
        raise NotImplementedError(b'A DateView must provide an implementation of get_dated_items()')

    def get_dated_queryset(self, ordering=None, **lookup):
        """
        Get a queryset properly filtered according to `allow_future` and any
        extra lookup kwargs.
        """
        qs = self.get_queryset().filter(**lookup)
        date_field = self.get_date_field()
        allow_future = self.get_allow_future()
        allow_empty = self.get_allow_empty()
        paginate_by = self.get_paginate_by(qs)
        if ordering is not None:
            qs = qs.order_by(ordering)
        if not allow_future:
            now = timezone.now() if self.uses_datetime_field else timezone_today()
            qs = qs.filter(**{b'%s__lte' % date_field: now})
        if not allow_empty:
            is_empty = len(qs) == 0 if paginate_by is None else not qs.exists()
            if is_empty:
                raise Http404(_(b'No %(verbose_name_plural)s available') % {b'verbose_name_plural': force_text(qs.model._meta.verbose_name_plural)})
        return qs

    def get_date_list_period(self):
        """
        Get the aggregation period for the list of dates: 'year', 'month', or 'day'.
        """
        return self.date_list_period

    def get_date_list(self, queryset, date_type=None, ordering=b'ASC'):
        """
        Get a date list by calling `queryset.dates()`, checking along the way
        for empty lists that aren't allowed.
        """
        date_field = self.get_date_field()
        allow_empty = self.get_allow_empty()
        if date_type is None:
            date_type = self.get_date_list_period()
        date_list = queryset.dates(date_field, date_type, ordering)
        if date_list is not None and not date_list and not allow_empty:
            name = force_text(queryset.model._meta.verbose_name_plural)
            raise Http404(_(b'No %(verbose_name_plural)s available') % {b'verbose_name_plural': name})
        return date_list


class BaseArchiveIndexView(BaseDateListView):
    """
    Base class for archives of date-based items.

    Requires a response mixin.
    """
    context_object_name = b'latest'

    def get_dated_items(self):
        """
        Return (date_list, items, extra_context) for this request.
        """
        qs = self.get_dated_queryset(ordering=b'-%s' % self.get_date_field())
        date_list = self.get_date_list(qs, ordering=b'DESC')
        if not date_list:
            qs = qs.none()
        return (date_list, qs, {})


class ArchiveIndexView(MultipleObjectTemplateResponseMixin, BaseArchiveIndexView):
    """
    Top-level archive of date-based items.
    """
    template_name_suffix = b'_archive'


class BaseYearArchiveView(YearMixin, BaseDateListView):
    """
    List of objects published in a given year.
    """
    date_list_period = b'month'
    make_object_list = False

    def get_dated_items(self):
        """
        Return (date_list, items, extra_context) for this request.
        """
        year = self.get_year()
        date_field = self.get_date_field()
        date = _date_from_string(year, self.get_year_format())
        since = self._make_date_lookup_arg(date)
        until = self._make_date_lookup_arg(self._get_next_year(date))
        lookup_kwargs = {b'%s__gte' % date_field: since, 
           b'%s__lt' % date_field: until}
        qs = self.get_dated_queryset(ordering=(b'-%s' % date_field), **lookup_kwargs)
        date_list = self.get_date_list(qs)
        if not self.get_make_object_list():
            qs = qs.none()
        return (date_list, qs,
         {b'year': date, 
            b'next_year': self.get_next_year(date), 
            b'previous_year': self.get_previous_year(date)})

    def get_make_object_list(self):
        """
        Return `True` if this view should contain the full list of objects in
        the given year.
        """
        return self.make_object_list


class YearArchiveView(MultipleObjectTemplateResponseMixin, BaseYearArchiveView):
    """
    List of objects published in a given year.
    """
    template_name_suffix = b'_archive_year'


class BaseMonthArchiveView(YearMixin, MonthMixin, BaseDateListView):
    """
    List of objects published in a given year.
    """
    date_list_period = b'day'

    def get_dated_items(self):
        """
        Return (date_list, items, extra_context) for this request.
        """
        year = self.get_year()
        month = self.get_month()
        date_field = self.get_date_field()
        date = _date_from_string(year, self.get_year_format(), month, self.get_month_format())
        since = self._make_date_lookup_arg(date)
        until = self._make_date_lookup_arg(self._get_next_month(date))
        lookup_kwargs = {b'%s__gte' % date_field: since, 
           b'%s__lt' % date_field: until}
        qs = self.get_dated_queryset(**lookup_kwargs)
        date_list = self.get_date_list(qs)
        return (
         date_list, qs,
         {b'month': date, 
            b'next_month': self.get_next_month(date), 
            b'previous_month': self.get_previous_month(date)})


class MonthArchiveView(MultipleObjectTemplateResponseMixin, BaseMonthArchiveView):
    """
    List of objects published in a given year.
    """
    template_name_suffix = b'_archive_month'


class BaseWeekArchiveView(YearMixin, WeekMixin, BaseDateListView):
    """
    List of objects published in a given week.
    """

    def get_dated_items(self):
        """
        Return (date_list, items, extra_context) for this request.
        """
        year = self.get_year()
        week = self.get_week()
        date_field = self.get_date_field()
        week_format = self.get_week_format()
        week_start = {b'%W': b'1', 
           b'%U': b'0'}[week_format]
        date = _date_from_string(year, self.get_year_format(), week_start, b'%w', week, week_format)
        since = self._make_date_lookup_arg(date)
        until = self._make_date_lookup_arg(self._get_next_week(date))
        lookup_kwargs = {b'%s__gte' % date_field: since, 
           b'%s__lt' % date_field: until}
        qs = self.get_dated_queryset(**lookup_kwargs)
        return (
         None, qs,
         {b'week': date, 
            b'next_week': self.get_next_week(date), 
            b'previous_week': self.get_previous_week(date)})


class WeekArchiveView(MultipleObjectTemplateResponseMixin, BaseWeekArchiveView):
    """
    List of objects published in a given week.
    """
    template_name_suffix = b'_archive_week'


class BaseDayArchiveView(YearMixin, MonthMixin, DayMixin, BaseDateListView):
    """
    List of objects published on a given day.
    """

    def get_dated_items(self):
        """
        Return (date_list, items, extra_context) for this request.
        """
        year = self.get_year()
        month = self.get_month()
        day = self.get_day()
        date = _date_from_string(year, self.get_year_format(), month, self.get_month_format(), day, self.get_day_format())
        return self._get_dated_items(date)

    def _get_dated_items(self, date):
        """
        Do the actual heavy lifting of getting the dated items; this accepts a
        date object so that TodayArchiveView can be trivial.
        """
        lookup_kwargs = self._make_single_date_lookup(date)
        qs = self.get_dated_queryset(**lookup_kwargs)
        return (
         None, qs,
         {b'day': date, 
            b'previous_day': self.get_previous_day(date), 
            b'next_day': self.get_next_day(date), 
            b'previous_month': self.get_previous_month(date), 
            b'next_month': self.get_next_month(date)})


class DayArchiveView(MultipleObjectTemplateResponseMixin, BaseDayArchiveView):
    """
    List of objects published on a given day.
    """
    template_name_suffix = b'_archive_day'


class BaseTodayArchiveView(BaseDayArchiveView):
    """
    List of objects published today.
    """

    def get_dated_items(self):
        """
        Return (date_list, items, extra_context) for this request.
        """
        return self._get_dated_items(datetime.date.today())


class TodayArchiveView(MultipleObjectTemplateResponseMixin, BaseTodayArchiveView):
    """
    List of objects published today.
    """
    template_name_suffix = b'_archive_day'


class BaseDateDetailView(YearMixin, MonthMixin, DayMixin, DateMixin, BaseDetailView):
    """
    Detail view of a single object on a single date; this differs from the
    standard DetailView by accepting a year/month/day in the URL.
    """

    def get_object(self, queryset=None):
        """
        Get the object this request displays.
        """
        year = self.get_year()
        month = self.get_month()
        day = self.get_day()
        date = _date_from_string(year, self.get_year_format(), month, self.get_month_format(), day, self.get_day_format())
        qs = queryset or self.get_queryset()
        if not self.get_allow_future() and date > datetime.date.today():
            raise Http404(_(b'Future %(verbose_name_plural)s not available because %(class_name)s.allow_future is False.') % {b'verbose_name_plural': qs.model._meta.verbose_name_plural, 
               b'class_name': self.__class__.__name__})
        lookup_kwargs = self._make_single_date_lookup(date)
        qs = qs.filter(**lookup_kwargs)
        return super(BaseDetailView, self).get_object(queryset=qs)


class DateDetailView(SingleObjectTemplateResponseMixin, BaseDateDetailView):
    """
    Detail view of a single object on a single date; this differs from the
    standard DetailView by accepting a year/month/day in the URL.
    """
    template_name_suffix = b'_detail'


def _date_from_string(year, year_format, month=b'', month_format=b'', day=b'', day_format=b'', delim=b'__'):
    """
    Helper: get a datetime.date object given a format string and a year,
    month, and day (only year is mandatory). Raise a 404 for an invalid date.
    """
    format = delim.join((year_format, month_format, day_format))
    datestr = delim.join((year, month, day))
    try:
        return datetime.datetime.strptime(datestr, format).date()
    except ValueError:
        raise Http404(_(b"Invalid date string '%(datestr)s' given format '%(format)s'") % {b'datestr': datestr, 
           b'format': format})


def _get_next_prev(generic_view, date, is_previous, period):
    """
    Helper: Get the next or the previous valid date. The idea is to allow
    links on month/day views to never be 404s by never providing a date
    that'll be invalid for the given view.

    This is a bit complicated since it handles different intervals of time,
    hence the coupling to generic_view.

    However in essence the logic comes down to:

        * If allow_empty and allow_future are both true, this is easy: just
          return the naive result (just the next/previous day/week/month,
          reguardless of object existence.)

        * If allow_empty is true, allow_future is false, and the naive result
          isn't in the future, then return it; otherwise return None.

        * If allow_empty is false and allow_future is true, return the next
          date *that contains a valid object*, even if it's in the future. If
          there are no next objects, return None.

        * If allow_empty is false and allow_future is false, return the next
          date that contains a valid object. If that date is in the future, or
          if there are no next objects, return None.

    """
    date_field = generic_view.get_date_field()
    allow_empty = generic_view.get_allow_empty()
    allow_future = generic_view.get_allow_future()
    get_current = getattr(generic_view, b'_get_current_%s' % period)
    get_next = getattr(generic_view, b'_get_next_%s' % period)
    start, end = get_current(date), get_next(date)
    if allow_empty:
        if is_previous:
            result = get_current(start - datetime.timedelta(days=1))
        else:
            result = end
        if allow_future or result <= timezone_today():
            return result
        return
    else:
        if is_previous:
            lookup = {b'%s__lt' % date_field: generic_view._make_date_lookup_arg(start)}
            ordering = b'-%s' % date_field
        else:
            lookup = {b'%s__gte' % date_field: generic_view._make_date_lookup_arg(end)}
            ordering = date_field
        if not allow_future:
            if generic_view.uses_datetime_field:
                now = timezone.now()
            else:
                now = timezone_today()
            lookup[b'%s__lte' % date_field] = now
        qs = generic_view.get_queryset().filter(**lookup).order_by(ordering)
        try:
            result = getattr(qs[0], date_field)
        except IndexError:
            return

        if generic_view.uses_datetime_field:
            if settings.USE_TZ:
                result = timezone.localtime(result)
            result = result.date()
        return get_current(result)
    return


def timezone_today():
    """
    Return the current date in the current time zone.
    """
    if settings.USE_TZ:
        return timezone.localtime(timezone.now()).date()
    else:
        return datetime.date.today()