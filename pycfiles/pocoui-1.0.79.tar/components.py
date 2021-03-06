# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/highlight/components.py
# Compiled at: 2006-12-26 17:17:53
__doc__ = '\n    pocoo.pkg.highlight.components\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n    Pocoo connection for the highlighter.\n\n    :copyright: 2006 by Georg Brandl.\n    :license: GNU GPL, see LICENSE for more details.\n'
from pocoo import Component
from pocoo.application import Page
from pocoo.http import Response
from pocoo.template import FileRequirements
from pocoo.pkg.core.bbcode import BBCodeTagProvider
from pocoo.utils.html import unescape_html
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments import highlight

def get_lexers(ctx):
    """
    Return a list of ``(key, title)`` tuples of known lexers.
    """
    lexers = []
    for (name, aliases, _, _) in get_all_lexers():
        lexers.append((aliases[0], name))

    lexers.sort(key=lambda x: x[1].lower())
    return lexers


class HighlightingBBCodeTagProvider(Page, FileRequirements, BBCodeTagProvider):
    """
    Render ``[code=lexername]`` BBCode tags and make the HTML formatter
    stylesheet and "toggle lineno" JS known + serve them.

    """
    __module__ = __name__
    formatter = HtmlFormatter(style='pastie', encoding='utf-8')
    handler_regexes = ['!highlight_bbcode_css$']

    def get_node(self, token, parser):
        if token.name == 'code' and token.attr:
            code = unescape_html(parser.get_tokens('/code').flatten())
            code = code.expandtabs(8).lstrip('\n').rstrip()
            try:
                lexer = get_lexer_by_name(token.attr)
            except ValueError:
                return
            else:
                code = highlight(code, lexer, self.formatter)
                return code.decode('utf-8')

    def get_buttons(self, req):
        _ = req.gettext
        return [{'tagname': 'code', 'name': _('Sourcecode'), 'description': _('Insert highlighted sourcecode'), 'insert': '[code={attr}]{text}[/code]', 'values': get_lexers(self.ctx)}]

    def get_stylesheet_imports(self):
        return [
         '/!highlight_bbcode_css']

    def handle_request(self, req):
        return Response(self.formatter.get_style_defs(), [('Content-Type', 'text/css')])