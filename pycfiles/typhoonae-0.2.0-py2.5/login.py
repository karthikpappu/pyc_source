# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/handlers/login.py
# Compiled at: 2010-12-12 04:36:57
"""Login/logout handler."""
import Cookie, base64, cookielib, google.appengine.ext.webapp, md5, os, re, socket, urllib2, wsgiref.handlers

def getCookieName():
    """Returns the cookie name.

    To get the appcfg upload_data command work we have to provide the correct
    cookie name for easy authentication.

    TODO: This is a huge security hole and should be fixed for the productive
          environment.
    """
    if os.environ.get('HTTP_X_APPCFG_API_VERSION') == '1':
        return 'dev_appserver_login'
    else:
        return 'typhoonae_login'


def getUserInfo(cookie):
    """Get the user info from the HTTP cookie in the CGI environment."""
    c = Cookie.SimpleCookie(cookie)
    cookie_name = getCookieName()
    value = ''
    if cookie_name in c:
        value = c[cookie_name].value
    (email, admin, user_id) = (value.split(':') + ['', '', ''])[:3]
    return (
     email, admin == 'True', user_id)


def createLoginCookiePayload(email, admin):
    """Creates cookie payload data for login information."""
    admin_string = 'False'
    if admin:
        admin_string = 'True'
    if email:
        user_id_digest = md5.new(email.lower()).digest()
        user_id = '1' + ('').join([ '%02d' % ord(x) for x in user_id_digest ])[:20]
    else:
        user_id = ''
    return '%s:%s:%s' % (email, admin_string, user_id)


def createLoginCookie(email, admin):
    """Creates a login cookie."""
    return cookielib.Cookie(0, getCookieName(), createLoginCookiePayload(email, admin=admin), None, False, socket.getfqdn(), False, False, '/', True, False, None, True, None, None, {}, rfc2109=False)


def authenticate(email, admin=False):
    """Authenticate user with given email."""
    cj = cookielib.CookieJar()
    cj.set_cookie(createLoginCookie(email, admin=admin))
    urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)))


def getSetCookieHeaderValue(email, admin=False):
    """Returns header value for setting the login cookie."""
    cookie_name = getCookieName()
    c = Cookie.SimpleCookie()
    c[cookie_name] = createLoginCookiePayload(email, admin=admin)
    c[cookie_name]['path'] = '/'
    return str(re.compile('^Set-Cookie: ').sub('', c.output(), count=1))


class LoginRequestHandler(google.appengine.ext.webapp.RequestHandler):
    """Simple login handler."""

    def get(self):
        """Sets the authentication cookie."""
        next_url = self.request.get('continue', '/')
        if os.environ.get('HTTP_AUTHORIZATION', False):
            self.redirect(next_url)
            return
        self.response.headers.add_header('Set-Cookie', getSetCookieHeaderValue('admin@typhoonae', admin=True))
        self.response.set_status(401)
        self.response.headers.add_header('Content-Type', 'text/html')
        self.response.out.write('<html><body>You\'re logged in as admin@typhoonae! This is a demo login handler.<br><a href="%s">Continue</a></body></html>' % next_url)


class LogoutRequestHandler(google.appengine.ext.webapp.RequestHandler):
    """Simple logout handler."""

    def get(self):
        """Removes the authentication cookie."""
        cookie_name = getCookieName()
        c = Cookie.SimpleCookie()
        c[cookie_name] = ''
        c[cookie_name]['path'] = '/'
        c[cookie_name]['max-age'] = '0'
        h = re.compile('^Set-Cookie: ').sub('', c.output(), count=1)
        self.response.headers.add_header('Set-Cookie', str(h))
        self.redirect(self.request.get('continue', '/'))


app = google.appengine.ext.webapp.WSGIApplication([
 (
  '/_ah/login', LoginRequestHandler),
 (
  '/_ah/logout', LogoutRequestHandler)], debug=True)

def main():
    wsgiref.handlers.CGIHandler().run(app)


if __name__ == '__main__':
    main()