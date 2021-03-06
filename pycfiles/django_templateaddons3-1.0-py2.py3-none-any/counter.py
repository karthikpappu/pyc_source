# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: templateaddons/../templateaddons/templatetags/counter.py
# Compiled at: 2016-10-21 19:35:23
from django import template
from templateaddons.settings import TEMPLATEADDONS_COUNTERS_VARIABLE
from templateaddons.utils import decode_tag_arguments, parse_tag_argument
register = template.Library()

class Counter:

    def __init__(self, start=0, step=1, ascending=True):
        self.value = start
        self.start = start
        self.step = step
        self.ascending = ascending


class CounterNode(template.Node):

    def __init__(self, name='"default"', start=0, step=1, ascending=True, silent=False, assign=False):
        self.name = name
        self.start = start
        self.step = step
        self.ascending = ascending
        self.silent = silent
        self.assign = assign

    def render(self, context):
        if TEMPLATEADDONS_COUNTERS_VARIABLE not in context:
            context[TEMPLATEADDONS_COUNTERS_VARIABLE] = {}
        counters = context[TEMPLATEADDONS_COUNTERS_VARIABLE]
        name = parse_tag_argument(self.name, context)
        assign = parse_tag_argument(self.assign, context)
        if name not in counters:
            start = parse_tag_argument(self.start, context)
            step = parse_tag_argument(self.step, context)
            ascending = parse_tag_argument(self.ascending, context)
            counters[name] = Counter(start, step, ascending)
        elif counters[name].ascending:
            counters[name].value += counters[name].step
        else:
            counters[name].value -= counters[name].step
        context[TEMPLATEADDONS_COUNTERS_VARIABLE] = counters
        if assign:
            context[assign] = counters[name].value
        if self.silent:
            return ''
        else:
            return '%d' % counters[name].value


def counter(parser, token):
    default_arguments = {}
    default_arguments['name'] = '"default"'
    default_arguments['start'] = 0
    default_arguments['step'] = 1
    default_arguments['ascending'] = True
    default_arguments['silent'] = False
    default_arguments['assign'] = '""'
    arguments = decode_tag_arguments(token, default_arguments)
    return CounterNode(**arguments)


register.tag('counter', counter)