# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/models/search_scope.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 4712 bytes
import itertools, logging, os, posixpath
from pip._vendor.packaging.utils import canonicalize_name
import pip._vendor.six.moves.urllib as urllib_parse
from pip._internal.models.index import PyPI
from pip._internal.utils.compat import has_tls
from pip._internal.utils.misc import normalize_path, redact_auth_from_url
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import List
logger = logging.getLogger(__name__)

class SearchScope(object):
    __doc__ = '\n    Encapsulates the locations that pip is configured to search.\n    '

    @classmethod
    def create(cls, find_links, index_urls):
        """
        Create a SearchScope object after normalizing the `find_links`.
        """
        built_find_links = []
        for link in find_links:
            if link.startswith('~'):
                new_link = normalize_path(link)
                if os.path.exists(new_link):
                    link = new_link
            built_find_links.append(link)

        if not has_tls():
            for link in itertools.chain(index_urls, built_find_links):
                parsed = urllib_parse.urlparse(link)
                if parsed.scheme == 'https':
                    logger.warning('pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.')
                    break

        return cls(find_links=built_find_links,
          index_urls=index_urls)

    def __init__(self, find_links, index_urls):
        self.find_links = find_links
        self.index_urls = index_urls

    def get_formatted_locations(self):
        lines = []
        redacted_index_urls = []
        if self.index_urls:
            if self.index_urls != [PyPI.simple_url]:
                for url in self.index_urls:
                    redacted_index_url = redact_auth_from_url(url)
                    purl = urllib_parse.urlsplit(redacted_index_url)
                    if not purl.scheme:
                        if not purl.netloc:
                            logger.warning('The index url "{}" seems invalid, please provide a scheme.'.format(redacted_index_url))
                    redacted_index_urls.append(redacted_index_url)

                lines.append('Looking in indexes: {}'.format(', '.join(redacted_index_urls)))
        if self.find_links:
            lines.append('Looking in links: {}'.format(', '.join((redact_auth_from_url(url) for url in self.find_links))))
        return '\n'.join(lines)

    def get_index_urls_locations(self, project_name):
        """Returns the locations found via self.index_urls

        Checks the url_name on the main (first in the list) index and
        use this url_name to produce all locations
        """

        def mkurl_pypi_url(url):
            loc = posixpath.join(url, urllib_parse.quote(canonicalize_name(project_name)))
            if not loc.endswith('/'):
                loc = loc + '/'
            return loc

        return [mkurl_pypi_url(url) for url in self.index_urls]