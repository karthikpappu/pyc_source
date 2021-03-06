# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mardochee.macxis/Projects/Python/web-portfolio/webportfolio/ext.py
# Compiled at: 2015-11-03 12:25:20
"""
Extras
Contains some
"""
import re, warnings, logging, inspect, functools
from six.moves.urllib.parse import urlparse
from flask import abort, request, current_app
from core import WebPortfolio, init_app
import utils, humanize, wp_markdown, flask_cloudy, flask_recaptcha, flask_seasurf, flask_kvsession, flask_cache, flask_login, ses_mailer, flask_mail, flask_s3
__all__ = [
 'mailer',
 'cache',
 'storage',
 'recaptcha',
 'csrf']

def user_authenticated():
    """
    A shortcut to check if a user is authenticated
    :return: bool
    """
    if flask_login.current_user and flask_login.current_user.is_authenticated:
        return True
    return False


def user_not_authenticated():
    """
    A shortcut to check if user not authenticated.
    """
    return not user_authenticated()


def _setup(app):

    def sanity_check():
        keys = [
         'SECRET_KEY',
         'APPLICATION_ADMIN_EMAIL',
         'MAILER_URI',
         'MAILER_SENDER',
         'MODULE_CONTACT_PAGE_EMAIL',
         'RECAPTCHA_SITE_KEY',
         'RECAPTCHA_SECRET_KEY']
        for k in keys:
            if k not in app.config or not app.config.get(k) or app.config.get(k).strip() == '':
                msg = 'Config [ %s ] value is not set or empty' % k
                app.logger.warn(msg)

    sanity_check()
    WebPortfolio.g(APPLICATION_NAME=app.config.get('APPLICATION_NAME'), APPLICATION_VERSION=app.config.get('APPLICATION_VERSION'), APPLICATION_URL=app.config.get('APPLICATION_URL'), APPLICATION_GOOGLE_ANALYTICS_ID=app.config.get('APPLICATION_GOOGLE_ANALYTICS_ID'))

    @app.template_filter('datetime')
    def format_datetime(dt, format='%m/%d/%Y'):
        if not dt:
            return ''
        return dt.strftime(format)

    @app.template_filter('strip_decimal')
    def strip_decimal(amount):
        return amount.split('.')[0]

    @app.template_filter('bool_to_yes')
    def bool_to_yes(b):
        if b:
            return 'Yes'
        return 'No'

    @app.template_filter('bool_to_int')
    def bool_to_int(b):
        if b:
            return 1
        return 0

    @app.template_filter('nl2br')
    def nl2br(s):
        """
        {{ s|nl2br }}

        Convert newlines into <p> and <br />s.
        """
        if not isinstance(s, basestring):
            s = str(s)
        s = re.sub('\\r\\n|\\r|\\n', '\n', s)
        paragraphs = re.split('\n{2,}', s)
        paragraphs = [ '<p>%s</p>' % p.strip().replace('\n', '<br />') for p in paragraphs ]
        return ('\n\n').join(paragraphs)

    app.jinja_env.filters.update({'slug': utils.slugify, 
       'int_with_comma': humanize.intcomma, 
       'date_since': humanize.naturaldate, 
       'time_since': humanize.naturaltime, 
       'markdown': wp_markdown.html, 
       'markdown_toc': wp_markdown.toc})


init_app(_setup)

def _session(app):
    store = None
    uri = app.config.get('SESSION_URI')
    if uri:
        parse_uri = urlparse(uri)
        scheme = parse_uri.scheme
        username = parse_uri.username
        password = parse_uri.password
        hostname = parse_uri.hostname
        port = parse_uri.port
        bucket = parse_uri.path.strip('/')
        if 'redis' in scheme:
            import redis
            from simplekv.memory.redisstore import RedisStore
            conn = redis.StrictRedis.from_url(url=uri)
            store = RedisStore(conn)
        elif 's3' in scheme or 'google_storage' in scheme:
            from simplekv.net.botostore import BotoStore
            import boto
            if 's3' in scheme:
                _con_fn = boto.connect_s3
            else:
                _con_fn = boto.connect_gs
            conn = _con_fn(username, password)
            _bucket = conn.create_bucket(bucket)
            store = BotoStore(_bucket)
        elif 'memcache' in scheme:
            import memcache
            from simplekv.memory.memcachestore import MemcacheStore
            host_port = '%s:%s' % (hostname, port)
            conn = memcache.Client(servers=[host_port])
            store = MemcacheStore(conn)
        elif 'sql' in scheme:
            from simplekv.db.sql import SQLAlchemyStore
            from sqlalchemy import create_engine, MetaData
            engine = create_engine(uri)
            metadata = MetaData(bind=engine)
            store = SQLAlchemyStore(engine, metadata, 'kvstore')
            metadata.create_all()
        else:
            raise ValueError('Invalid Session Store')
    if store:
        flask_kvsession.KVSessionExtension(store, app)
    return


init_app(_session)

class _Mailer(object):
    """
    A simple wrapper to switch between SES-Mailer and Flask-Mail based on config
    """
    mail = None
    provider = None
    config = None
    _template = None

    def init_app(self, app):
        self.config = app.config
        scheme = None
        mailer_uri = self.config.get('MAILER_URI')
        if mailer_uri:
            mailer_uri = urlparse(mailer_uri)
            scheme = mailer_uri.scheme
            if 'ses' in scheme:
                self.provider = 'SES'
                access_key = mailer_uri.username or app.config.get('AWS_ACCESS_KEY_ID')
                secret_key = mailer_uri.password or app.config.get('AWS_SECRET_ACCESS_KEY')
                self.mail = ses_mailer.Mail(aws_access_key_id=access_key, aws_secret_access_key=secret_key, sender=self.config.get('MAILER_SENDER'), reply_to=self.config.get('MAILER_REPLY_TO'), template=self.config.get('MAILER_TEMPLATE'), template_context=self.config.get('MAILER_TEMPLATE_CONTEXT'))
            elif 'smtp' in scheme:
                self.provider = 'SMTP'

                class _App(object):
                    config = {'MAIL_SERVER': mailer_uri.hostname, 
                       'MAIL_USERNAME': mailer_uri.username, 
                       'MAIL_PASSWORD': mailer_uri.password, 
                       'MAIL_PORT': mailer_uri.port, 
                       'MAIL_USE_TLS': True if 'tls' in mailer_uri.scheme else False, 
                       'MAIL_USE_SSL': True if 'ssl' in mailer_uri.scheme else False, 
                       'MAIL_DEFAULT_SENDER': app.config.get('MAILER_SENDER'), 
                       'TESTING': app.config.get('TESTING'), 
                       'DEBUG': app.config.get('DEBUG')}
                    debug = app.config.get('DEBUG')
                    testing = app.config.get('TESTING')

                _app = _App()
                self.mail = flask_mail.Mail(app=_app)
                _ses_mailer = ses_mailer.Mail(template=self.config.get('MAILER_TEMPLATE'), template_context=self.config.get('MAILER_TEMPLATE_CONTEXT'))
                self._template = _ses_mailer.parse_template
            else:
                warnings.warn("Mailer Error. Invalid scheme '%s'>" % scheme)
        return

    def send(self, to, subject, body, reply_to=None, **kwargs):
        """
        Send simple message
        """
        if self.provider == 'SES':
            self.mail.send(to=to, subject=subject, body=body, reply_to=reply_to, **kwargs)
        elif self.provider == 'SMTP':
            msg = flask_mail.Message(recipients=[isinstance(to, list) or to] if 1 else to, subject=subject, body=body, reply_to=reply_to, sender=self.config.get('MAILER_SENDER'))
            self.mail.send(msg)
        else:
            abort(500, "Mailer Error. Invalid 'provider'")

    def send_template(self, template, to, reply_to=None, **context):
        """
        Send Template message
        """
        if self.provider == 'SES':
            self.mail.send_template(template=template, to=to, reply_to=reply_to, **context)
        elif self.provider == 'SMTP':
            data = self._template(template=template, **context)
            msg = flask_mail.Message(recipients=[isinstance(to, list) or to] if 1 else to, subject=data['subject'], body=data['body'], reply_to=reply_to, sender=self.config.get('MAILER_SENDER'))
            self.mail.send(msg)
        else:
            abort(500, "Mailer Error. Invalid 'provider'")


mailer = _Mailer()
init_app(mailer.init_app)

class _AssetsDelivery(flask_s3.FlaskS3):

    def init_app(self, app):
        delivery_method = app.config.get('ASSETS_DELIVERY_METHOD')
        if delivery_method and delivery_method.upper() in ('S3', 'CDN'):
            is_secure = False
            if delivery_method.upper() == 'CDN':
                domain = app.config.get('ASSETS_DELIVERY_DOMAIN')
                if '://' in domain:
                    domain_parsed = urlparse(domain)
                    is_secure = domain_parsed.scheme == 'https'
                    domain = domain_parsed.netloc
                app.config.setdefault('S3_CDN_DOMAIN', domain)
            app.config['FLASK_ASSETS_USE_S3'] = True
            app.config['USE_S3'] = True
            app.config.setdefault('S3_USE_HTTPS', is_secure)
            app.config['S3_URL_STYLE'] = 'path'
            app.config.setdefault('S3_ONLY_MODIFIED', False)
            app.config.setdefault('S3_BUCKET_NAME', app.config.get('AWS_S3_BUCKET_NAME'))
            super(self.__class__, self).init_app(app)


assets_delivery = _AssetsDelivery()
init_app(assets_delivery.init_app)
cache = flask_cache.Cache()
init_app(cache.init_app)
storage = flask_cloudy.Storage()
init_app(storage.init_app)
recaptcha = flask_recaptcha.ReCaptcha()
init_app(recaptcha.init_app)
csrf = flask_seasurf.SeaSurf()
init_app(csrf.init_app)