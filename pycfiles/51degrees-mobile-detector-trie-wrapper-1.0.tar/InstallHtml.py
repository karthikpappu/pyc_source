# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\DistExt\InstallHtml.py
# Compiled at: 2006-08-22 11:27:39
import os, re
from Ft.Lib import Uri
from Ft.Lib.DistExt import InstallDocs

class InstallHtml(InstallDocs.InstallDocs):
    __module__ = __name__
    command_name = 'install_html'
    description = 'install HTML documentation'
    output_extension = '.html'

    def finalize_options(self):
        if self.install_dir is None:
            install = self.get_finalized_command('install')
            self.install_dir = os.path.join(install.install_docs, 'html')
        return InstallDocs.InstallDocs.finalize_options(self)
        return

    def get_default_stylesheets(self):
        return {'docbook': 'docbook_html.xslt', 'sdocbook': 'sdocbook_html.xslt', 'modules': 'modules_html.xslt', 'extensions': 'extensions_html.xslt', 'commandline': 'commandline_html.xslt', 'docbook_html': 'docbook_html1.xslt'}

    def get_default_css(self):
        """
        Returns a mapping of stylesheet names to their associated CSS.

        The CSS file is assumed to be relative to the stylesheet URI.
        """
        return {'docbook': 'docbook_html.css', 'sdocbook': 'sdocbook_html.css', 'modules': 'modules.css', 'extensions': 'extensions.css', 'commandline': 'commandline.css'}

    def get_stylesheet_extras(self, stylesheet, base_uri):
        css = self.get_default_css().get(stylesheet)
        if css is None:
            return []

        def find_css_uris(uri):
            """Find all the CSS dependencies (@import directives)."""
            uris = [
             uri]
            stream = Uri.UrlOpen(uri)
            for line in Uri.UrlOpen(uri).readlines():
                match = re.match('\\s*@import\\s+url\\s*\\((.*)\\)', line)
                if match:
                    next_uri = Uri.BaseJoin(uri, eval(match.group(1)))
                    uris.extend(find_css_uris(next_uri))

            return uris

        return find_css_uris(Uri.BaseJoin(base_uri, css))
        return

    def get_output_filename(self, document):
        (basedir, basename) = os.path.split(document.source)
        basedir = basedir[len(self.build_dir) + len(os.sep):]
        (basename, source_ext) = os.path.splitext(basename)
        basename += self.output_extension
        return os.path.join(self.install_dir, basedir, basename)