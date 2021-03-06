# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/presenzialo/logs/dayutils/dayutils.py
# Compiled at: 2020-01-15 07:36:53
# Size of source mod 2**32: 3645 bytes
import datetime, calendar
__author__ = 'so07'
__version__ = '0.1.0'
fmt_id = '%Y%m%d'
fmt_time = '%H:%M:%S'
fmt_day = '%d/%m/%Y'
fmt_weekday = '%a'
fmt_idtot = fmt_id + fmt_time
fmt_tot = fmt_day + ' ' + fmt_time
fmt_human = fmt_day + ' ' + fmt_weekday
fmt_humantot = fmt_day + ' ' + fmt_time + ' ' + fmt_weekday
fmt_times = [
 '%H:%M:%S', '%H:%M', '%H.%M.%S', '%H%M%S', '%H.%M']
days_abbr = list(calendar.day_abbr)
days_long = list(calendar.day_name)
months_abbr = list(calendar.month_abbr)
months_long = list(calendar.month_name)

def date2day(dt, fmt=fmt_tot):
    return dt.strptime(dt.strftime(fmt), fmt)


def str2day(day):
    for fmt in [fmt_idtot, fmt_id]:
        try:
            datetime.datetime.strptime(day, fmt)
        except:
            pass
        else:
            return date2day(datetime.datetime.strptime(day, fmt), fmt)


def str2time(t):
    for fmt in fmt_times:
        try:
            datetime.datetime.strptime(t, fmt)
        except:
            pass
        else:
            return date2day(datetime.datetime.strptime(t, fmt), fmt).time()


def day_from_epoch(day):
    epoch = datetime.datetime.utcfromtimestamp(0)
    d = day - epoch
    return d.days


def sec_from_epoch(day):
    epoch = datetime.datetime.utcfromtimestamp(0)
    d = day - epoch
    return d.total_seconds()


class day_range:

    def __init__(self, start, end, step=datetime.timedelta(1)):
        self.start = start
        self.end = end
        self.step = step

    def __len__(self):
        return len([d for d in self])

    def __str__(self):
        return 'start : {}; end : {}'.format(self.start, self.end)

    def __iter__(self):
        self.this_day = self.start
        return self

    def __next__(self):
        this_day = self.this_day
        next_day = this_day + self.step
        if this_day > self.end:
            raise StopIteration
        self.this_day = next_day
        return this_day

    def start(self):
        return self.start

    def end(self):
        return self.end

    def step(self):
        return self.step

    def years(self):
        for y in sorted(set([i.year for i in self])):
            yield y

    def months(self):
        for m, y in sorted(set([(i.year, i.month) for i in self])):
            yield (
             m, y)

    def days(self):
        for i in self:
            yield (
             i.year, i.month, i.day)


def week_bounds(day):
    if isinstance(day, datetime.date):
        day = datetime.datetime.combine(day, datetime.datetime.min.time())
    start = day.date() - datetime.timedelta(days=(day.weekday()))
    end = start + datetime.timedelta(days=6)
    return (start, end)


def month_bounds(day):
    last_day_month = calendar.monthrange(day.year, day.month)[1]
    start = datetime.date(day.year, day.month, 1)
    end = datetime.date(day.year, day.month, last_day_month)
    return (start, end)


def month_weeks_bounds(day):
    w = calendar.Calendar().monthdatescalendar(day.year, day.month)
    return [(i[0], i[(-1)]) for i in w]


def is_same_month(date1, date2):
    if date1.year == date2.year:
        if date1.month == date2.month:
            return True
    return False


def sec2str(seconds):
    m, s = divmod(abs(seconds), 60)
    h, m = divmod(abs(m), 60)
    r = ''
    if seconds < 0:
        r += '-'
    r += '%02d:%02d:%02d' % (h, m, s)
    return r