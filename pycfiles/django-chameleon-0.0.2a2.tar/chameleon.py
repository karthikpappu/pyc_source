# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/django-chameleon/chameleon/templatetags/chameleon.py
# Compiled at: 2013-01-20 19:14:33
from __future__ import with_statement
from django.template import Node
from django.template import TemplateSyntaxError, Library
from django.conf import settings
register = Library()

class GetCurrentTheme(Node):
    """
    Template node class used by ``get_current_theme_tag``.
    """

    def __init__(self, variable):
        self.variable = variable

    def render(self, context):
        context['THEME_NAME'] = self.variable
        context['THEME_URL'] = settings.STATIC_URL + self.variable + '/'
        return ''


@register.tag('set_theme_id')
def get_current_theme_tag(parser, token):
    """
    Stores the name of the current theme name in the context.

    Usage::

        {% set_theme_id THEME_NAME %}

        ...

        <div>
            THEME_NAME: {{ THEME_NAME }}<br>
            THEME_URL): {{ THEME_URL }}<br>
            Example resource: <a href="{{ THEME_URL }}css/edit.css">Link</a>
        </div>

    This will fetch the currently active theme and put its name
    into the ``THEME_NAME`` context variable.  It will also make the THEME_URL variable available for other resource needs that may be relative to the path of the theme directory.

    """
    args = token.contents.split()
    if len(args) != 2:
        raise TemplateSyntaxError("'set_theme_id' requires a valid 'theme name' (got %r)" % args)
    return GetCurrentTheme(args[1])