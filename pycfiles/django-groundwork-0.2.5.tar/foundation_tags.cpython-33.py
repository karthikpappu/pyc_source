# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ben/repos/bip2/foundation/templatetags/foundation_tags.py
# Compiled at: 2014-04-27 18:20:21
# Size of source mod 2**32: 2371 bytes
from django import template
from django.templatetags.static import static
from django.contrib.messages import constants
register = template.Library()

@register.simple_tag
def foundation_js(js_name=None):
    """
    Use this tag to create static foundation script includes.
    """
    js_path = 'foundation/js/foundation/foundation.{0}.js'.format(js_name)
    if js_name is None:
        js_path = 'foundation/js/foundation.min.js'.format(js_name)
    return '<script src="{0}"></script>'.format(static(js_path))


@register.simple_tag
def foundation_vendor(vendor_name):
    """
    Use this tag to create static foundation vendor script includes.
    """
    vendor_path = 'foundation/js/vendor/{0}.js'.format(vendor_name)
    return '<script src="{0}"></script>'.format(static(vendor_path))


@register.simple_tag
def foundation_css(css_name):
    """
    Use this tag to create static stylesheet includes.
    """
    css_path = 'foundation/css/{0}.css'.format(css_name)
    return '<link rel="stylesheet" href="{0}"/>'.format(static(css_path))


@register.simple_tag
def foundation_icon(icon_name, size=None, classes=None):
    """
    Use this tag to render foundation icons, you can specify extra classes
    and/or a font-size attribute.
    """
    if size:
        size = 'style="font-size:{0}"'.format(size)
    else:
        size = ''
    if not classes:
        classes = ''
    return '<i {0} class="{1} {2}"></i>'.format(size, icon_name, classes)


@register.simple_tag
def foundation_alert(message, level=20):
    """
    Use this tag to translate a django.contrib.messages message into a
    foundation alert box with appropriate icon and style for the message
    type
    """
    icon = 'fi-info'
    alert_class = ''
    if level == constants.INFO:
        icon = 'fi-info'
    if level == constants.DEBUG:
        icon = 'fi-alert'
        alert_class = 'info'
    if level == constants.SUCCESS:
        icon = 'fi-check'
        alert_class = 'success'
    if level == constants.WARNING:
        icon = 'fi-alert'
        alert_class = 'warning'
    if level == constants.ERROR:
        icon = 'fi-x'
        alert_class = 'warning'
    return '<div data-alert class="alert-box {0} radius" >\n{1}&nbsp;\n{2}\n{3}</div>'.format(alert_class, foundation_icon(icon, size='20px'), message, '<a href="#" class="close">&times</a>')