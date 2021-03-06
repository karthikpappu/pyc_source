# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\tests\test_toscawidgets.py
# Compiled at: 2011-07-14 07:28:12
"""Tests for integration of ToscaWidgets with TurboGears."""
import re
from turbogears import config, controllers, expose, testutil
try:
    from tw.api import CSSLink, CSSSource, JSLink, JSSource, WidgetsList, locations as tw_locations
    from tw.forms import TableForm, TextField
except ImportError, e:
    import warnings
    warnings.warn('ToscaWidgets not installed. Can not perform TG integration unit tests!: %s' % e)
else:
    css_link = CSSLink(modname='turbogears.tests', filename='foo.css')
    css_src = CSSSource('body {font-size: 1.em;}')
    js_link = JSLink(modname='turbogears.tests', filename='foo.js')
    js_head_src = JSSource("alert('head');")
    js_headbottom_src = JSSource("alert('headbottom');", location=tw_locations.headbottom)
    js_bodytop_src = JSSource("alert('bodytop');", location=tw_locations.bodytop)
    js_bodybottom_src = JSSource("alert('bodybottom');", location=tw_locations.bodybottom)
    rx_css_link = '<link.*?href=".*?%s".*?>'
    rx_js_link = '<script.*?src=".*?%s".*?>'
    rx_css_src = '<style.*?>\\s*?%s\\s*?</style>'
    rx_js_src = '<script.*?>\\s*?%s\\s*?</script>'

    class FormWithResources(TableForm):
        __module__ = __name__

        class fields(WidgetsList):
            __module__ = __name__
            title = TextField()

        javascript = [
         js_link, js_head_src, js_headbottom_src, js_bodytop_src, js_bodybottom_src]
        css = [
         css_link, css_src]

        def retrieve_javascript(self):
            raise NotImplementedError

        def retrieve_css(self):
            raise NotImplementedError


    form = FormWithResources()

    class MyRoot(controllers.RootController):
        __module__ = __name__

        @expose('turbogears.tests.form')
        def show_form(self):
            return dict(form=form)

        @expose('kid:turbogears.tests.form')
        def show_form_kid(self):
            return dict(form=form)

        @expose('turbogears.tests.form')
        def show_table_form(self):
            return dict(form=TableForm())


    class ToscaWidgetsTest(testutil.TGTest):
        __module__ = __name__
        root = MyRoot

        def setUp(self):
            self.defaultview = config.get('tg.defaultview', 'kid')
            config.update({'toscawidgets.on': True, 'tg.defaultview': 'genshi'})
            super(ToscaWidgetsTest, self).setUp()

        def tearDown(self):
            super(ToscaWidgetsTest, self).tearDown()
            config.update({'toscawidgets.on': False, 'tg.defaultview': self.defaultview})

        def test_css_inclusion(self):
            """Inclusion of CSS widgets in Genshi templates works with ToscaWidgets."""
            response = self.app.get('/show_form')
            assert re.search(rx_css_src % 'body \\{font-size: 1\\.em;\\}', response.body)
            assert re.search(rx_css_link % 'foo\\.css', response.body)

        def test_js_inclusion(self):
            """Inclusion of JS widgets in Genshi templates works with ToscaWidgets."""
            response = self.app.get('/show_form')
            for src in ("alert\\('head'\\);", "alert\\('headbottom'\\);", "alert\\('bodytop'\\);",
                        "alert\\('bodybottom'\\);"):
                assert re.search(rx_js_src % src, response.body)

            assert re.search(rx_js_link % 'foo\\.js', response.body)

        def test_css_inclusion_kid(self):
            """Inclusion of CSS widgets in Kid templates works with ToscaWidgets."""
            response = self.app.get('/show_form_kid')
            assert re.search(rx_css_src % 'body \\{font-size: 1\\.em;\\}', response.body)
            assert re.search(rx_css_link % 'foo\\.css', response.body)

        def test_js_inclusion_kid(self):
            """Inclusion of JS widgets in Kid templates works with ToscaWidgets."""
            response = self.app.get('/show_form_kid')
            for src in ("alert\\('head'\\);", "alert\\('headbottom'\\);", "alert\\('bodytop'\\);",
                        "alert\\('bodybottom'\\);"):
                assert re.search(rx_js_src % src, response.body)

            assert re.search(rx_js_link % 'foo\\.js', response.body)

        def test_include_widgets(self):
            """Any widget can be included everywhere by setting tg.include_widgets."""
            config.update({'global': {'tg.include_widgets': ['turbogears.tests.test_toscawidgets.js_link', 'turbogears.tests.test_toscawidgets.css_src']}})
            response = self.app.get('/show_table_form')
            config.update({'global': {'tg.include_widgets': []}})
            assert 'foo.js' in response
            assert 'body {font-size: 1.em;}' in response
            assert 'foo.css' not in response
            assert "alert('head');" not in response