# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_localize/views/catalogue.py
# Compiled at: 2014-05-04 12:45:31
"""Catalogue view."""
import sys, os, time, logging, subprocess
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path
from pyramid.httpexceptions import HTTPFound
from pyramid_localize.tools import destination_path
from pyramid_localize.tools import set_localizer
logger = logging.getLogger(__name__)

@view_defaults(permission='manage_translations', renderer='pyramid_localize:resources/templates/index.mako')
class CatalogueView(object):
    """View class for catalogue manipulation actions."""

    def __init__(self, request):
        """
        Assign request.

        :param pyramid.request.Request request:
        """
        self.request = request

    def _translation_file(self, language, domain, extension='po'):
        """
        Create a translation file path.

        :param str language: two-letter language code
        :param str domain: translation domain name
        :param str extension: translation file extension (po/mo)
        """
        translation_destination = destination_path(self.request)
        return os.path.abspath(os.path.join(translation_destination, language, 'LC_MESSAGES', domain + '.' + extension))

    def _translation_template_path(self, spec):
        """
        Calculate path to translation template file.

        :param str spec: either full path, or package related path
        """
        (package_name, filename) = resolve_asset_spec(spec)
        if package_name is None:
            return os.path.abspath(filename)
        else:
            __import__(package_name)
            package = sys.modules[package_name]
            return os.path.abspath(os.path.join(package_path(package), filename))
            return

    @view_config(route_name='localize:index')
    def index(self):
        """
        Simple action listing domains, and its files of files with metadata.

        :returns:

            .. code-block:: python

                {
                    'language': {
                        'domain1': {
                            'po': 'modification time',
                            'pot': 'modification time',
                            'mo': 'modification time',
                            },
                        # more domains
                    },
                    # more languages
                }
        """
        translations = {}
        translation_sources = self.request.registry['config'].localize.translation.sources
        for language in self.request.registry['config'].localize.locales.available:
            translations[language] = {}
            for domain in translation_sources:
                translations[language][domain] = {'po': None, 'pot': None, 
                   'mo': None}
                po_file = self._translation_file(language, domain)
                if os.path.isfile(po_file):
                    translations[language][domain]['po'] = time.ctime(os.path.getmtime(po_file))
                pot_file = self._translation_template_path(translation_sources[domain])
                if os.path.isfile(pot_file):
                    translations[language][domain]['pot'] = time.ctime(os.path.getmtime(pot_file))
                mo_file = self._translation_file(language, domain, 'mo')
                if os.path.isfile(mo_file):
                    translations[language][domain]['mo'] = time.ctime(os.path.getmtime(mo_file))

        return {'translations': translations}

    @view_config(route_name='localize:update')
    def update_catalogue(self):
        """
        Update or initialize translation catalogues.

        Create (.po files) for each language/catalogue from their respective
        translation templates (.pot). This action is performed for every language
        defined within `localize.locales.available` config key.

        Redirects itself to **localize:index**.
        """
        self.index()
        translation_sources = self.request.registry['config'].localize.translation.sources
        for domain in translation_sources:
            pot_file = self._translation_template_path(translation_sources[domain])
            if not os.path.isfile(pot_file):
                logger.critical(('pot file for {domain} does not exists!').format(domain=domain))
            for language in self.request.registry['config'].localize.locales.available:
                po_file = self._translation_file(language, domain)
                if os.path.isfile(po_file):
                    logger.debug(('po file for {domain}, {language} exists, proceeding with update').format(domain=domain, language=language))
                    if subprocess.call([self.request.registry['config'].localize.pybabel,
                     'update',
                     '-l', language,
                     '-i', pot_file,
                     '-o', po_file,
                     '--previous']):
                        logger.error(('Error while trying to update {po} file!').format(po=po_file))
                else:
                    logger.debug(('po file for {domain}, {language} does not exists,\n                         proceeding with initialize').format(domain=domain, language=language))
                    if subprocess.call([self.request.registry['config'].localize.pybabel,
                     'init',
                     '-l', language,
                     '-i', pot_file,
                     '-o', po_file]):
                        logger.error(('Error while trying to update {po} file!').format(po=po_file))

        return HTTPFound(location=self.request.route_url('localize:index'))

    @view_config(route_name='localize:compile')
    def compile_catalogue(self):
        """
        Compile all translation files.

        For every language defined compile .po files into into .mo file that's used by gettext.

        Redirects to **localize:index**.
        """
        self.index()
        translation_sources = self.request.registry['config'].localize.translation.sources
        for domain in translation_sources:
            for language in self.request.registry['config'].localize.locales.available:
                po_file = self._translation_file(language, domain)
                mo_file = self._translation_file(language, domain, 'mo')
                if os.path.isfile(po_file):
                    logger.debug(('po file for {domain}, {language} exists,\n                        proceeding with compilation').format(domain=domain, language=language))
                    if subprocess.call([self.request.registry['config'].localize.pybabel,
                     'compile',
                     '-l', language,
                     '-i', po_file,
                     '-o', mo_file,
                     '--use-fuzzy']):
                        logger.error(('Error while trying to compile {po} file!').format(po=po_file))

        return HTTPFound(location=self.request.route_url('localize:index'))

    @view_config(route_name='localize:reload', xhr='True', renderer='json')
    @view_config(route_name='localize:reload')
    def reload_catalogue(self):
        """
        Reload translation catalogue for application it's run in.

        .. note::

            To see how is this happening, you might want to see
            :func:`~pyramid_localize.tools.set_localizer`

        :returns:

            Only for xhr requests:

            .. code-block:: python

                {
                    'status': True,
                    'msg': 'Localizators has been reloaded' # translated
                }

            non xhr requests: Redirects to **localize:index**.

        """
        set_localizer(self.request, True)
        if self.request.is_xhr:
            return {'status': True, 'msg': self.request._('Localizators has been reloaded')}
        return HTTPFound(location=self.request.route_url('localize:index'))