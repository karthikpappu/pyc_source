# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wareweb/interfaces.py
# Compiled at: 2006-10-22 17:17:11
"""
Descriptions of the main interfaces in Wareweb.  These aren't formal
interfaces, they are just here for documentation purposes.
"""

class Attribute(object):
    __module__ = __name__
    __pudge_visible__ = False

    def __init__(self, doc):
        self.__doc__ = doc


class IServlet:
    """
    Response method sequence
    ------------------------

    These methods are called roughly in order to produce the response.
    """
    __module__ = __name__

    def __call__(environ, start_response):
        """
        Implementation of the WSGI application interface.

        Instances of IServlet are WSGI applications.

        Calls event ``call`` with ``environ`` and ``start_response``,
        which may return (status_headers, app_iter) and thus abort the
        rest of the call.
        """
        pass

    def run():
        """
        'Runs' the request.

        This typically just calls ``awake()``, ``respond()`` and
        ``sleep()``.  Error handlers could be added here by
        subclasses.
        
        Wrapped as event (wrapped methods call ``start_method_name``
        and ``end_method_name``).
        """
        pass

    def awake(call_setup=True):
        """
        Called at beginning of request.

        SHOULD NOT produce output.  If ``call_setup`` is true then
        ``.setup()`` will be called.  ``SitePage`` classes (that is,
        abstract subclasses of ``Servlet``) should override this
        method and not ``setup``.
        
        Wrapped as event.
        """
        pass

    def setup():
        """
        Also called at beginning of requests.

        Subclasses do not need to call the superclass implementation.
        This is where individual (non-abstract) servlets typically do
        their setup.
        """
        pass

    def respond():
        """
        Called after ``.awake()``, this typically produces the body of the response.

        Some components may intercept this method (e.g., components
        that want to take over the body of the response, like
        templating components).  Wrapped as event.
        """
        pass

    def sleep(call_teardown=True):
        """
        Called at the end of a request, to clean up resources.

        Called regardless of exceptions in ``.awake()`` or
        ``.respond()``, so implementations should be careful not to
        assume all resources have been successfully set up.  Like
        ``awake`` this calls ``.teardown()`` if ``call_teardown`` is
        true; abstract classes should override this method and not
        ``teardown``.

        Wrapped as event.
        """
        pass

    def teardown():
        """
        Resource cleanup at the end of request.

        Subclasses do not need to call the superclass implementation.
        """
        pass

    environ = Attribute('\n    The WSGI environment.\n\n    Contains typical CGI variables, in addition to any WSGI\n    extensions.\n    ')
    config = Attribute('\n    The Paste configuration object; a dictionary-like object.\n    ')
    app_url = Attribute('\n    The URL (usually not fully qualified) of this application.\n\n    This looks in the environmental variable ``<app_name>.base_url``.\n    The default ``app_name`` is ``"app"``, and this requires a\n    ``urlparser_hook`` in ``__init__.py`` to set accurately, which\n    would look like::\n\n        app_name = \'app\'\n        def urlparse_hook(environ):\n            key = \'%s.base_url\' % app_name\n            if not key in environ:\n                environ[key] = environ[\'SCRIPT_NAME\']\n    ')
    path_info = Attribute("\n    The value of ``environ['PATH_INFO']`` -- all the URL that comes\n    after this servlet's location.  ")
    path_parts = Attribute("\n    A list of path parts; essentially ``path_info.split('/')``\n    ")
    fields = Attribute('\n    A dictionary-like object of all the request fields (both GET and\n    POST variables, folded together).\n\n    You can also get variables as attributes (which default to None).\n\n    Also has a ``.getlist(name)`` method, which returns the variable\n    as a list (i.e., if missing the return value is ``[]``; if one\n    string value the return value is ``[value]``)\n    ')
    title = Attribute("\n    Attribute that returns the title of this page.  Default\n    implementation returns the class's name.\n    ")
    session = Attribute('\n    The session object.  This is a dictionary-like object where values\n    are persisted through multiple requests (using a cookie).\n    ')

    def set_cookie(cookie_name, value, path='/', expires='ONCLOSE', secure=False):
        """
        Creates the named cookie in the response.

        ``expires`` can be:
        
        * ``ONCLOSE`` (default: expires when browser is closed)
        * ``NOW`` (for immediate deletion)
        * ``NEVER`` (some time far in the future)
        * A integer value (expiration in seconds)
        * A time.struct_time object
        * A string that starts with ``+`` and describes the time, like
          ``+1w`` (1 week) or ``+1b`` (1 month)
        """
        pass

    def set_header(header_name, header_value):
        """
        Sets the named header; overwriting any header that previously
        existed.

        The ``Status`` header is specially used to change the response
        status.
        """
        pass

    def add_header(header_name, header_value):
        """
        Adds the named header, appending to any previous header that
        might have been set.
        """
        pass

    def write(*objs):
        """
        Writes the objects.

        ``None`` is written as the empty string, and unicode objects
        are encoded with UTF-8.
        """
        pass

    def redirect(url, **query_vars):
        """
        Redirects to the given URL.  If the URL is relative, then it
        will be resolved to be absolute with respect to
        ``self.app_url``.

        The status is 303 by default; a status keyword argument can be
        passed to override this.

        Other variables are appended to the query string, e.g.::

            self.redirect('edit', id=5)

        Will redirect to ``edit?id=5``
        """
        pass