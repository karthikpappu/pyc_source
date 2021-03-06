# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/renderers.py
# Compiled at: 2016-04-18 08:06:52
# Size of source mod 2**32: 1819 bytes
from __future__ import unicode_literals
from api_star.compat import text_type, COMPACT_SEPARATORS, VERBOSE_SEPARATORS
from api_star.decorators import annotate
from api_star.utils import JSONEncoder
from coreapi.codecs import CoreJSONCodec
import jinja2, json

def json_renderer(verbose=False, ensure_ascii=False, encoder_cls=None):
    if verbose:
        separators = VERBOSE_SEPARATORS
        indent = 4
    else:
        separators = COMPACT_SEPARATORS
        indent = None
    if encoder_cls is None:
        encoder_cls = JSONEncoder

    @annotate(media_type='application/json', charset=None, format='json')
    def renderer(data, **context):
        content = json.dumps(data, separators=separators, indent=indent, cls=encoder_cls, ensure_ascii=ensure_ascii)
        if isinstance(content, text_type):
            content = content.encode('utf-8')
        return content

    return renderer


def corejson_renderer(verbose=False):
    codec = CoreJSONCodec()

    @annotate(media_type='application/vnd.coreapi+json', charset=None, format='coreapi')
    def renderer(data, **context):
        return codec.dump(data, indent=verbose)

    return renderer


def docs_renderer(template=None):
    if template is None:
        loader = jinja2.PackageLoader('api_star', 'templates')
        env = jinja2.Environment(loader=loader)
        template = env.get_template('docs.html')

    @annotate(media_type='text/html', charset='utf-8', format='html')
    def renderer(data, **context):
        return template.render(document=data)

    return renderer


def html_renderer():

    @annotate(media_type='text/html', charset='utf-8', format='html')
    def renderer(data, **context):
        return data

    return renderer