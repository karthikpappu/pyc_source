# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\floscraper\webscraper.py
# Compiled at: 2019-08-03 22:41:47
"""
Module for loading/scraping data from the web
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'the01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2014-19, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.1.11'
__date__ = b'2019-08-04'
import re, socket
from bs4 import BeautifulSoup
import html2text, requests
from requests import HTTPError
from requests.exceptions import SSLError, Timeout, ConnectionError
from flotils.loadable import Loadable
from .default_user_agents import default_user_agents
from .models import Response, CacheInfo
from .cache import FileCache, NullCache

class WEBParameterException(Exception):
    """ Parameter Exception """
    pass


class WEBFileException(IOError):
    """ File Exception """
    pass


class WEBConnectException(Exception):
    """ Error with web connection """
    pass


class WebScraper(Loadable):
    """ Class for cached, session get/post/.. with optional scraping """

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings for instance (default: None)
        :type settings: dict | None
        :rtype: None
        """
        if settings is None:
            settings = {}
        super(WebScraper, self).__init__(settings)
        self.url = settings.get(b'url', None)
        self.scheme = settings.get(b'scheme', None)
        self.timeout = settings.get(b'timeout', None)
        cache_sett = settings.get(b'cache')
        self.cache = NullCache()
        if cache_sett:
            self.cache = FileCache(cache_sett)
        self._auth_method = settings.get(b'auth_method', None)
        self._auth_username = settings.get(b'auth_username', None)
        self._auth_password = settings.get(b'auth_password', None)
        self.session = None
        self._handle_redirect = settings.get(b'handle_redirect', True)
        agent_browser = default_user_agents[b'browser'][b'keith']
        agent_os = default_user_agents[b'os'][b'linux_i686']
        agent = settings.get(b'user_agent', None)
        if b'default_user_agents_browser' in settings:
            brow = settings[b'default_user_agents_browser']
            agent_browser = default_user_agents[b'browser'].get(brow, None)
        if b'default_user_agents_os' in settings:
            os = settings[b'default_user_agents_os']
            agent_os = default_user_agents[b'os'].get(os, None)
        if b'user_agent_browser' in settings:
            agent_browser = settings[b'user_agent_browser']
        if b'user_agent_os' in settings:
            agent_os = settings[b'user_agent_os']
        if not agent:
            if agent_browser and agent_os:
                agent = agent_browser.format(agent_os)
        self.user_agent = agent
        self._text_maker = None
        if settings.get(b'html2text'):
            self._set_html2text(settings[b'html2text'])
        self.html_parser = settings.get(b'html_parser', b'html.parser')
        return

    def _browser_init(self):
        """
        Init the browsing instance if not setup

        :rtype: None
        """
        if self.session:
            return
        else:
            self.session = requests.Session()
            headers = {}
            if self.user_agent:
                headers[b'User-agent'] = self.user_agent
            self.session.headers.update(headers)
            if self._auth_method in (None, '', 'HTTPBasicAuth'):
                if self._auth_username is not None:
                    self.session.auth = (
                     self._auth_username, self._auth_password)
            return

    def _set_html2text(self, settings):
        """
        Load settings for html2text (https://github.com/Alir3z4/html2text)

        Warning: does not check options/values

        :param settings: Settings for the object
            (see:https://github.com/Alir3z4/html2text/blob/master/docs/usage.md)
        :type settings: dict
        :rtype: None
        """
        self._text_maker = html2text.HTML2Text()
        for param in settings:
            if not hasattr(self._text_maker, param):
                raise WEBParameterException((b'Setting html2text failed - unknown parameter {}').format(param))
            setattr(self._text_maker, param, settings[param])

    def load_scrap(self, path):
        """
        Load scraper settings from file

        :param path: Path to file
        :type path: str
        :rtype: None
        :raises WEBFileException: Failed to load settings
        :raises WEBParameterException: Missing parameters in file
        """
        try:
            conf = self.load_settings(path)
        except:
            self.exception(b'Failed to load file')
            raise WEBFileException((b'Failed to load from {}').format(path))

        if b'scheme' not in conf:
            raise WEBParameterException(b'Missing scheme definition')
        if b'url' not in conf:
            raise WEBParameterException(b'Missing url definition')
        version = conf.get(b'version', None)
        if version != b'1.0':
            raise WEBParameterException((b'Unsupported version {}').format(version))
        self.scheme = conf[b'scheme']
        self.url = conf[b'url']
        self.timeout = conf.get(b'timeout', self.timeout)
        if conf.get(b'html2text'):
            self._set_html2text(conf[b'html2text'])
        return

    def request(self, method, url, timeout=None, headers=None, data=None, params=None):
        """
        Make a request using the requests library

        :param method: Which http method to use (GET/POST)
        :type method: str | unicode
        :param url: Url to make request to
        :type url: str | unicode
        :param timeout: Timeout for request (default: None)
            None -> infinite timeout
        :type timeout: None | int | float
        :param headers: Headers to be passed along (default: None)
        :type headers: None | dict
        :param data: Data to be passed along (e.g. body in POST)
            (default: None)
        :type data: None | dict
        :param params: Parameters to be passed along (e.g. with url in GET)
            (default: None)
        :type params: None | dict
        :return: Response to the request
        :rtype: requests.Response
        :raises WEBConnectException: Loading failed
        """
        if headers is None:
            headers = {}
        if not self.session:
            self._browser_init()
        try:
            response = self.session.request(method, url, timeout=timeout, allow_redirects=self._handle_redirect, headers=headers, data=data, params=params)
        except SSLError as e:
            raise WEBConnectException(e)
        except HTTPError:
            raise WEBConnectException((b'Unable to load {}').format(url))
        except (Timeout, socket.timeout):
            raise WEBConnectException((b'Timeout loading {}').format(url))
        except ConnectionError:
            raise WEBConnectException((b'Failed to load {}').format(url))
        except Exception:
            self.exception((b'Failed to load {}').format(url))
            raise WEBConnectException((b'Unknown failure loading {}').format(url))

        return response

    def _get(self, url, **kwargs):
        """
        Make GET request

        :param url: Url to make the request to
        :type url: str | unicode
        :param kwargs: See _requests for parameters
        :type kwargs:
        :return: Response
        :rtype: requests.Response
        """
        return self.request(b'GET', url, **kwargs)

    def _post(self, url, **kwargs):
        """
        Make POST request

        :param url: Url to make the request to
        :type url: str | unicode
        :param kwargs: See _requests for parameters
        :type kwargs: dict
        :return: Response
        :rtype: requests.Response
        """
        return self.request(b'POST', url, **kwargs)

    def get(self, url, timeout=None, headers=None, params=None, cache_ext=None):
        """
        Make get request to url (might use cache)

        :param url: Url to make request to
        :type url: str | unicode
        :param timeout: Timeout for request (default: None)
            None -> infinite timeout
        :type timeout: None | int | float
        :param headers: Headers to be passed along (default: None)
        :type headers: None | dict
        :param params: Parameters to be passed along with url (default: None)
        :type params: None | dict
        :param cache_ext: External cache info
        :type cache_ext: floscraper.models.CacheInfo
        :return: Response
        :rtype: floscraper.models.Response | None
        :raises WEBConnectException: Loading failed
        """
        if headers is None:
            headers = {}
        cached = cache_info = None
        if self.cache:
            cached, cache_info = self.cache.get(url)
        if cache_ext:
            if not cache_info:
                cache_info = cache_ext
            if cache_info.access_time and cache_ext.access_time:
                if cache_info.access_time < cache_ext.access_time:
                    cached = None
                    cache_info = cache_ext
            if cache_info.etag != cache_ext.etag:
                cached = None
                cache_info = cache_ext
        if cached:
            if cache_info:
                cache_info.hit = True
            return Response(cached, cache_info)
        if cache_info:
            cache_info.hit = None
        if not self.session:
            self._browser_init()
        if self.cache:
            headers = self.cache.prepare_headers(headers, cache_info)
        response = self._get(url, timeout=timeout, headers=headers, params=params)
        if b'etag' in response.headers:
            if not cache_info:
                cache_info = CacheInfo()
            cache_info.etag = response.headers.get(b'etag')
        res = Response(cache_info=cache_info)
        if cache_info:
            cache_info.hit = False
        if response.history:
            code = 0
            for resp in response.history + [None]:
                if resp is None:
                    resp = response
                if code in [
                 requests.codes.FOUND,
                 requests.codes.SEE_OTHER,
                 requests.codes.TEMPORARY_REDIRECT]:
                    self.info((b'Temporary redirect to {}').format(resp.url))
                elif code in [
                 requests.codes.MOVED_PERMANENTLY,
                 requests.codes.PERMANENT_REDIRECT]:
                    self.warning((b'Moved to {}').format(resp.url))
                elif code != 0:
                    self.error((b'Code {} to {}').format(code, resp.url))
                code = resp.status_code

        if response.status_code == requests.codes.NOT_MODIFIED:
            self.info((b'Not modified {}').format(url))
            res.html, _ = self.cache.get(url, ignore_access_time=True)
            if cache_info:
                cache_info.hit = True
            if self.cache:
                self.cache.update(url, cache_info)
            return res
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise WEBConnectException((b'{} - {}').format(e, url))

        try:
            raw = response.content
            html = response.text
            if raw is None:
                self.warning(b'Response returned None')
                raise Exception()
            if html is None:
                self.warning(b'Response parsed returned None')
                raise Exception()
        except Exception:
            raise WEBConnectException((b'Unable to load {}').format(url))

        if self.cache:
            self.cache.put(url, html, cache_info)
        if url != response.url:
            if not response.history:
                self.warning((b'Response url different despite no redirects {} - {}').format(url, response.url))
            if self.cache:
                self.cache.put(response.url, html, cache_info)
        res.html = html
        res.raw = raw
        return res

    def _get_tag_match(self, ele, tree):
        """
        Match tag

        :param ele:
        :type ele:
        :param tree:
        :type tree: None, list
        :return:
        :rtype: None | list
        """
        if tree in [None, []]:
            return [ele]
        else:
            res = []
            t = tree[0]
            branch = tree[1:]
            attributes = {}
            for attr in t:
                if isinstance(t[attr], dict):
                    if t[attr].get(b'type', None) == b'reg':
                        t[attr] = re.compile(t[attr][b'reg'])

            attributes.update(t)
            if b'name' in attributes:
                del attributes[b'name']
            if b'text' in attributes:
                del attributes[b'text']
            if b'recursive' in attributes:
                del attributes[b'recursive']
            if b'[]' in attributes:
                del attributes[b'[]']
            possibles = ele.find_all(t.get(b'name', None), text=t.get(b'text', None), attrs=attributes, recursive=t.get(b'recursive', True))
            if not possibles:
                return
            if b'[]' in t:
                try:
                    possibles = eval((b'possibles[{}]').format(t[b'[]']))
                except:
                    return

            if not isinstance(possibles, list):
                possibles = [
                 possibles]
            for a in possibles:
                match = self._get_tag_match(a, branch)
                if match:
                    res.extend(match)

            if not res:
                return
            return res
            return

    def _parse_value(self, eles, value_scheme):
        """

        :param eles:
        :type eles: list
        :param value_scheme:
        :type value_scheme: dict
        :return:
        :rtype: list
        """
        val = []
        val_type = value_scheme.get(b'type', None)
        reg = value_scheme.get(b'reg', None)
        strip = value_scheme.get(b'strip', False)
        for match in eles:
            if val_type == b'text':
                val.append((b'{}').format(match.getText()))
            elif val_type == b'content':
                val.append((b'{}').format(match.getText()))
            elif val_type == b'attribute' and value_scheme.get(b'attribute', None):
                attr = value_scheme[b'attribute']
                if attr in match.attrs:
                    res = match[attr]
                    if isinstance(res, list):
                        res = (b' ').join(res)
                    val.append(res)
            elif val_type == b'html':
                val.append((b'{}').format(match))
            elif self._text_maker is None:
                val.append(html2text.html2text((b'{}').format(match)))
            else:
                val.append(self._text_maker.handle((b'{}').format(match)))
            if strip:
                val[-1] = val[(-1)].strip()

        if reg:
            res = []
            for a in val:
                if isinstance(reg, dict):
                    if reg.get(b'type', None) == b'reg':
                        reg = re.compile(reg[b'reg'])
                res.extend(reg.findall(a))

        else:
            res = val
        return res

    def _parse_scheme(self, ele, scheme):
        """

        :param ele:
        :type ele:
        :param scheme:
        :type scheme: dict[str | unicode, dict]
        :return:
        :rtype: dict
        """
        res = {}
        for aKey in scheme:
            entity = scheme[aKey]
            val = []
            matches = []
            res[aKey] = []
            if b'tree' in entity:
                matches = self._get_tag_match(ele, entity[b'tree'])
                if not matches:
                    matches = []
            if not matches and b'value' == aKey:
                val.extend(self._parse_value([ele], entity))
                res[aKey].extend(val)
            if b'value' == aKey:
                for a in matches:
                    val.extend(self._parse_value([ele], entity))

            if b'children' in entity:
                for a in matches:
                    obj = {}
                    if b'value' == aKey:
                        obj[b'value'] = val
                    child = self._parse_scheme(a, entity[b'children'])
                    if child:
                        obj.update(child)
                    if obj:
                        res[aKey].append(obj)

        return res

    def scrap(self, url=None, scheme=None, timeout=None, html_parser=None, cache_ext=None):
        """
        Scrap a url and parse the content according to scheme

        :param url: Url to parse (default: self._url)
        :type url: str
        :param scheme: Scheme to apply to html (default: self._scheme)
        :type scheme: dict
        :param timeout: Timeout for http operation (default: self._timout)
        :type timeout: float
        :param html_parser: What html parser to use (default: self._html_parser)
        :type html_parser: str | unicode
        :param cache_ext: External cache info
        :type cache_ext: floscraper.models.CacheInfo
        :return: Response data from url and parsed info
        :rtype: floscraper.models.Response
        :raises WEBConnectException: HTTP get failed
        :raises WEBParameterException: Missing scheme or url
        """
        if not url:
            url = self.url
        if not scheme:
            scheme = self.scheme
        if not timeout:
            timeout = self.timeout
        if not html_parser:
            html_parser = self.html_parser
        if not scheme:
            raise WEBParameterException(b'Missing scheme definition')
        if not url:
            raise WEBParameterException(b'Missing url definition')
        resp = self.get(url, timeout, cache_ext=cache_ext)
        soup = BeautifulSoup(resp.html, html_parser)
        resp.scraped = self._parse_scheme(soup, scheme)
        return resp

    def _shrink_list(self, shrink):
        """
        Shrink list down to essentials

        :param shrink: List to shrink
        :type shrink: list
        :return: Shrunk list
        :rtype: list
        """
        res = []
        if len(shrink) == 1:
            return self.shrink(shrink[0])
        for a in shrink:
            temp = self.shrink(a)
            if temp:
                res.append(temp)

        return res

    def _shrink_dict(self, shrink):
        """
        Shrink dict down to essentials

        :param shrink: Dict to shrink
        :type shrink: dict
        :return: Shrunk dict
        :rtype: dict
        """
        res = {}
        if len(shrink.keys()) == 1 and b'value' in shrink:
            return self.shrink(shrink[b'value'])
        for a in shrink:
            res[a] = self.shrink(shrink[a])
            if not res[a]:
                del res[a]

        return res

    def shrink(self, shrink):
        """
        Remove unnecessary parts

        :param shrink: Object to shringk
        :type shrink: dict | list
        :return: Shrunk object
        :rtype: dict | list
        """
        if isinstance(shrink, list):
            return self._shrink_list(shrink)
        if isinstance(shrink, dict):
            return self._shrink_dict(shrink)
        return shrink