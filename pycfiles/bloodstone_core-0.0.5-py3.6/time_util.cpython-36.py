# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wmpy_util/time_util.py
# Compiled at: 2020-01-08 03:03:37
# Size of source mod 2**32: 12320 bytes
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-19 14:33
@File    : time_util.py
@Desc    : 时间日期，计时工具等
"""
import time, datetime
from collections import Iterable, Iterator
from wmpy_util.print_util import *
DATETIME_FORMATER = '%Y-%m-%d %H:%M:%S'
DATE_FORMATER = '%Y-%m-%d'
DATETIME_FORMATER_YmdHM = '%Y-%m-%d %H:%M'
DATETIME_FORMATER_mdHM = '%m-%d %H:%M'
DATETIME_FORMATER_mdH = '%m-%d %Hh'
DATETIME_FORMATER_md = '%m-%d'
DATETIME_FORMATER_dH = '%dd-%Hh'
DATETIME_FORMATER_HM = '%H:%M'
DATETIME_FORMATER_MS = '%M:%S'
FORMAT_LIST = [
 DATETIME_FORMATER,
 DATE_FORMATER]
__all__ = [
 'ForTimer', 'GeneratorTimer', 'timer', 'SimpleTimer', 'get_datetime_by_str',
 'get_str_by_timestamp', 'get_str_by_datetime', 'generator_timer']

class FuncTimer:
    __doc__ = '\n    用于统计某个函数运行时间的类\n    使用@timer注解装饰需要统计时间的函数\n    不带参调用方式\n    @timer\n    def func():\n        ...\n    直接对函数进行统计，并取函数名作为识别名称\n\n    带参调用方式\n    @timer(name="test1", batch=100)\n    def func():\n        ...\n    指定函数识别名称为"test1", 并指定统计方式为合并模式，每一百次调用统计一次耗时\n    '

    def __init__(self):
        pass

    def timer(self, name='', batch=1, *args, **kwargs):
        """
        注解计时器
        :param name: 自定义打印名称，缺省时自动取函数名
        :param batch: 是否统计多次后一起打印，batch<1时，每次运行函数均打印计时
        :param args:
        :param kwargs:
        :return:
        """
        _name = name

        def decorator(func):
            if _name == '':
                _FuncTimer__name = func.__qualname__
            else:
                _FuncTimer__name = _name

            def wrapper(*args, **kwargs):
                start = time.time()
                ret = func(*args, **kwargs)
                now = time.time()
                _time_spend = (now - start) * 1000
                if batch > 1:
                    add_record(_FuncTimer__name, _time_spend, batch)
                else:
                    print('%s timeUsed = %s' % (_FuncTimer__name, smart_time(_time_spend)))
                return ret

            wrapper.__qualname__ = _FuncTimer__name
            wrapper.__name__ = _FuncTimer__name.split('.')[(-1)]
            return wrapper

        if callable(name):
            _func = name
            _name = _func.__qualname__
            decorator = decorator(_func)
        return decorator

    def generator_timer(self, name='', batch=1, *args, **kwargs):
        """
        正确处理一个Iterator生成函数的计时问题
        e.g.
        @generator_timer
        def get_generator(x):
            for i in range(x):
                yield x*x

        如果使用@timer注释，只能得到get_generator函数运行时间（只会执行一次）
        使用@generator_timer注释可以得到Iterator每次生产数据所花费的时间
        即，__next__()函数调用花费的时间

        :param name:
        :param batch:
        :return:
        """
        _name = name

        def decorator(func):
            if _name == '':
                _FuncTimer__name = func.__qualname__
            else:
                _FuncTimer__name = _name

            def wrapper(*args, **kwargs):
                start = time.time()
                generator = func(*args, **kwargs)
                now = time.time()
                _time_spend = (now - start) * 1000
                print('%s timeUsed = %s' % (_FuncTimer__name, smart_time(_time_spend)))
                return GeneratorTimer(generator, name=_FuncTimer__name, batch=batch)

            wrapper.__qualname__ = _FuncTimer__name
            wrapper.__name__ = _FuncTimer__name.split('.')[(-1)]
            return wrapper

        if callable(name):
            _func = name
            _name = _func.__qualname__
            decorator = decorator(_func)
        return decorator


class GeneratorTimer(Iterator, Iterable):

    def __init__(self, iter_obj, name='', batch=1):
        """
        对一个迭代器进行包装，并对迭代器生成数据进行计时，相当于调用__next__函数的耗时
        :param iter_obj:
        :param name:
        :param batch:
        """
        self.iterable_obj = None
        self.iterator_obj = None
        if isinstance(iter_obj, Iterable):
            self.iterable_obj = iter_obj
            self.iterator_obj = iter_obj.__iter__()
        else:
            if isinstance(iter_obj, Iterator):
                self.iterator_obj = iter_obj
            else:
                raise ValueError('iter_obj must be Iterable or Iterator!')
            if name:
                self.name = name
            else:
                self.name = iter_obj.__class__.__name__
        self.show_name = '{}::generator_data'.format(self.name)
        self.batch = batch

    def __iter__(self):
        if self.iterable_obj is not None:
            self.iterator_obj = self.iterable_obj.__iter__()
        return self

    def __next__(self):
        start = time.time()
        ret = self.iterator_obj.__next__()
        now = time.time()
        _time_spend = (now - start) * 1000
        if self.batch > 1:
            add_record(self.show_name, _time_spend, self.batch)
        else:
            print('%s timeUsed = %s' % (self.show_name, smart_time(_time_spend)))
        return ret


class ForTimer(GeneratorTimer):

    def __init__(self, iterable_obj, name='', batch=1):
        """
        for循环计时器
        对for循环进行计时，统计一整个大循环的耗时，相当于相邻两次调用__next__函数的时间差
        计时器织入的方式尽量减少侵入性
        原代码：
        for i in range(100):
            code line 1
            code line 2
             ...
            code line n

        织入for循环计时器:
         for i in ForTimer(range(100)):
            code line 1
            code line 2
             ...
            code line n

        不影响整体代码，对循环进行计时
        :param iterable_obj:
        :param name:
        :param batch:
        """
        super().__init__(iterable_obj, name, batch)
        self.last_time_stamp = None
        self.show_name = '{}::for_loop'.format(self.name)

    def __next__(self):
        cur_time = time.time()
        if self.last_time_stamp is not None:
            _time_spend = (cur_time - self.last_time_stamp) * 1000
            if self.batch > 1:
                add_record(self.show_name, _time_spend, self.batch)
            else:
                print('%s timeUsed = %s' % (self.show_name, smart_time(_time_spend)))
        self.last_time_stamp = cur_time
        try:
            ret = self.iterator_obj.__next__()
            return ret
        except StopIteration as exception:
            print('%s loop %s' % (self.show_name, UseStyle('end', font_color=color_red)))
            raise exception


class SimpleTimer:

    def __init__(self):
        """
        simple timer for code lines
        >> stimer = SimpleTimer()
        >> code 1
        >> code 2
        >> stimer.check("test1")
        >> code 3
        >> stimer.check("test2")
        """
        self._timestamp = time.time()

    def reset(self):
        self._timestamp = time.time()

    def check(self, name, reset=True):
        _now = time.time()
        _spend = (_now - self._timestamp) * 1000
        if reset:
            self._timestamp = _now
        print('%s timeUsed = %s' % (name, smart_time(_spend)))


_time_record = {}

def add_record(name, time_spend, batch):
    """
    是否会有线程安全问题？
    :param name:
    :param time_spend:
    :param batch:
    :return:
    """
    if name not in _time_record:
        record = dict(sum_time=0, iter_time=0, iter=0)
        _time_record[name] = record
    else:
        record = _time_record[name]
    record['sum_time'] += time_spend
    record['iter_time'] += time_spend
    record['iter'] += 1
    if record['iter'] % batch == 0:
        _iter_time, _iter = record['iter_time'], record['iter']
        _cost_ave = _iter_time / batch
        print('%s timeSpend %s/%s on %d/%d iterations, average cost=%s' % (
         name, smart_time(_iter_time), smart_time(record['sum_time']), batch, _iter, smart_time(_cost_ave)))
        record['iter_time'] = 0


_func_timer = FuncTimer()
timer = _func_timer.timer
generator_timer = _func_timer.generator_timer

def smart_time(milli_sec):
    if milli_sec < 10:
        time_format = '{:.2f} ms'.format(milli_sec)
    else:
        if milli_sec < 100:
            time_format = '{:.1f} ms'.format(milli_sec)
        else:
            if milli_sec < 1000:
                time_format = '{:.0f} ms'.format(milli_sec)
            else:
                if milli_sec < 10000:
                    time_format = '{:.2f} s'.format(milli_sec / 1000)
                else:
                    if milli_sec < 60000:
                        time_format = '{:.1f} s'.format(milli_sec / 1000)
                    else:
                        if milli_sec < 3600000:
                            secs = milli_sec / 1000 % 60
                            mins = int(milli_sec / 60 / 1000)
                            time_format = '{:d}m:{:2.0f}s'.format(mins, secs)
                        else:
                            secs = milli_sec / 1000 % 60
                            mins = milli_sec / 1000 / 60 % 60
                            hour = milli_sec / 1000 / 60 / 60
                            time_format = '{:.0f}h:{:2.0f}m:{:2.0f}s'.format(hour, mins, secs)
    return UseStyle(time_format, mode=mode_bold, font_color=color_blue)


def get_timestamp_by_str(date_str, _format=None):
    if _format is not None:
        return time.mktime(time.strptime(date_str, _format))
    else:
        time_obj = None
        try:
            time_obj = time.strptime(date_str, DATETIME_FORMATER)
        except ValueError as e:
            pass

        if time_obj is None:
            try:
                time_obj = time.strptime(date_str, DATE_FORMATER)
            except ValueError as e:
                pass

        if time_obj is None:
            return 0
        return time.mktime(time_obj)


def get_datetime_by_str(date_str, format=DATETIME_FORMATER):
    """

    :param date_str:
    :return:
    """
    if not date_str:
        return
    else:
        _datetime_obj = None
        format_list = FORMAT_LIST
        if format:
            format_list = [
             format]
        for format in format_list:
            try:
                _datetime_obj = datetime.datetime.strptime(date_str, format)
            except Exception as error:
                pass

            if _datetime_obj:
                break

        return _datetime_obj


def get_str_by_timestamp(timestamp=None, date_format=DATETIME_FORMATER):
    """
    将时间戳转为指定格式的字符串
    :param timestamp:
    :param format:
    :return:
    """
    if timestamp is None:
        timestamp = time.time()
    time_obj = time.localtime(timestamp)
    return time.strftime(date_format, time_obj)


def get_str_by_datetime(datetime_obj, format=DATETIME_FORMATER):
    """
    将datetime对象转为指定格式的字符串
    :param timestamp:
    :param format:
    :return:
    """
    datetime_str = None
    try:
        datetime_str = datetime.datetime.strftime(datetime_obj, format)
    except Exception as error:
        pass

    return datetime_str


@generator_timer
def fun(x):
    for i in range(x):
        yield i


if __name__ == '__main__':
    import math
    ts = math.sqrt(2)
    for i in ForTimer(range(10)):
        ts = ts * 2
        print(smart_time(ts))