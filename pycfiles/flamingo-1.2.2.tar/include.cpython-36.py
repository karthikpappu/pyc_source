# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/rst/include.py
# Compiled at: 2020-02-08 07:33:40
# Size of source mod 2**32: 1835 bytes
import logging
from docutils.parsers.rst import Directive, directives
from docutils.nodes import raw
from flamingo.core.utils.html import extract_section_by_title, TitleNotFoundError
from flamingo.plugins.rst.base import parse_rst
logger = logging.getLogger('flamingo.plugins.rst.parser.include')

class Section(Directive):
    required_arguments = 1
    has_content = True

    def run(self):
        content = '<div class="section" id="{}">{}</div>'.format(self.arguments[0], parse_rst(self.content))
        return [
         raw('', content, format='html')]


def include(context):

    class Include(Directive):
        has_content = False
        required_arguments = 1
        option_spec = {'title': directives.unchanged}

        def run(self):
            if 'title' not in self.options:
                raise ValueError('Invalid options')
            else:
                path = self.arguments[0]
                content = context.contents.get(path=path)
                if not content['content_body']:
                    context.parse(content)
                if 'title' in self.options:
                    title = self.options['title'].strip()
                    try:
                        html = extract_section_by_title(content['content_body'], title)
                    except TitleNotFoundError:
                        logger.error("%s: '%s' has no headline '%s'", context.content['path'], path, title)
                        return []

            return [raw('', html, format='html')]

    return Include


class rstInclude:

    def parser_setup(self, context):
        directives.register_directive('inc', include(context))