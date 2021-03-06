# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/clue/app/server.py
# Compiled at: 2008-06-27 12:03:50
import pkg_resources, logging, optparse, os, sys
from paste import httpserver
from paste import urlmap
from paste import urlparser
from genshi.template import loader as templateloader
from pysqlite2 import dbapi2 as sqlite
from clue.app import config
from clue.app import controller
from clue.app import environinit
from clue.app import patches
from clue.app import pdbcheck
from clue.app import redirect
from clue.app import utils
from clue.secure import auth
from clue.themer import theme

class Server(object):
    """A server for handling application requests."""

    def __init__(self, workingdir, should_pdb, logger=logging):
        self.workingdir = workingdir
        self.should_pdb = should_pdb
        self.logger = logger
        self._iter_count = 1
        dist = pkg_resources.get_distribution('ClueMapper')
        self.version = dist.version

    def serve_forever(self):
        patches.patch()
        while self._iter_count > 0:
            self._run()
            self._iter_count -= 1

        patches.unpatch()
        self.logger.info('ClueMapper v%s gracefully shut down' % self.version)

    def _run(self):
        global_conf = {}
        wsgi_app = make_app(global_conf, workingdir=self.workingdir, should_pdb=self.should_pdb)
        cluemapperconfig = global_conf['cluemapper.config']
        host = cluemapperconfig['base'].get('host', '0.0.0.0')
        port = cluemapperconfig['base'].get('port', '8080')
        server_address = (host, int(port))
        server = httpserver.WSGIServer(wsgi_app, server_address, httpserver.WSGIHandler)
        hoststr = host
        if hoststr == '0.0.0.0':
            hoststr = 'ALL INTERFACES'
        configfilename = os.path.realpath(cluemapperconfig.filename)
        curdir = os.path.realpath(os.curdir)
        if configfilename.startswith(curdir):
            configfilename = configfilename[len(curdir) + 1:]
        self.logger.info('ClueMapper v%s successfully started' % self.version)
        self.logger.info('Using configuration at %r' % configfilename)
        self.logger.info('Listening on %s, port %s' % (hoststr, port))
        self._listen(server)

    def _listen(self, server):
        server.socket.settimeout(3)
        self._run_inner = True
        try:
            while self._run_inner:
                server.handle_request()

        except KeyboardInterrupt:
            self._iter_count = 0
            self.logger.info('Shutting down...')

        server.socket.close()

    def reload(self):
        self.logger.info('Reloading server')
        self._iter_count += 1
        self._run_inner = False


def get_metadata():
    dist = pkg_resources.get_distribution('ClueMapper')
    pkginfo = dist.get_metadata('PKG-INFO')
    metadata = {}
    last_key = None
    last_value = ''
    for x in pkginfo.split('\n'):
        if not x.strip():
            last_value += '\n' + x.rstrip()
        elif not x.startswith(' '):
            if last_key is not None:
                metadata[last_key] = last_value.rstrip()
                last_key = ''
                last_value = ''
            (last_key, v) = x.split(':', 1)
            last_value += '\n' + v.strip()
        else:
            last_value += '\n' + x[8:].rstrip()

    if last_key is not None:
        metadata[last_key] = last_value[8:].rstrip()
    return metadata


def make_app(global_config, workingdir, should_pdb=None):
    pb = utils.PathBuilder(workingdir)
    themesdir = pb(os.path.join('etc', 'cluemapper', 'themes'))
    if not os.path.exists(themesdir):
        os.makedirs(themesdir)
    cluemapperconfig = config.load_config(workingdir)
    pkgloader = templateloader.package('clue.app', 'templates')
    loader = templateloader.TemplateLoader([pkgloader], auto_reload=True)
    global_config.update({'cluemapper.config': cluemapperconfig, 'cluemapper.workingdir': workingdir, 
       'cluemapper.templateloader': loader, 
       'cluemapper.metadata': get_metadata()})
    if 'defaulttheme' in cluemapperconfig['base']:
        global_config['cluemapper.defaultthemeid'] = cluemapperconfig['base']['defaulttheme']
    main = controller.make_app(global_config)
    authfile = pb(cluemapperconfig['base']['auth_file'])
    main = auth.make_filter(main, global_config, authfile=authfile)
    main = theme.make_filter(main, global_config)
    main = environinit.make_filter(main, global_config)
    mainredirect = redirect.make_app(global_config, main_redirect='/pm/', relative_redirect='/pm/p/')
    app = urlmap.URLMap()
    app['/'] = mainredirect
    app['/pm'] = main
    app['/.defaulttheme'] = urlparser.make_pkg_resources(global_config, 'ClueMapperThemer', 'clue/themer/defaulttheme')
    app['/.userthemes'] = urlparser.make_static(global_config, themesdir)
    app['/logout'] = main
    if should_pdb:
        app = pdbcheck.make_filter(app, global_config)
    ensure_existing(workingdir, cluemapperconfig)
    return app


def ensure_existing(workingdir, cluemapperconfig):
    pb = utils.PathBuilder(workingdir)
    authfile = pb(cluemapperconfig['base']['auth_file'])
    if not os.path.exists(authfile):
        f = open(authfile, 'w')
        f.close()
    shared_db = pb(os.path.join('etc', 'cluemapper', 'cluemapper.db'))
    if not os.path.exists(shared_db):
        cnx = sqlite.connect(shared_db)
        cursor = cnx.cursor()
        cursor.execute('CREATE TABLE user_info (username varchar(20), name varchar(50), value varchar(100))')
        cnx.commit()


def get_possible_workingdirs(executable):
    checks = [
     os.path.join(os.path.dirname(executable), '..'),
     sys.prefix,
     os.path.sep]
    res = []
    for x in checks:
        x = os.path.abspath(os.path.realpath(x))
        if x not in res:
            res.append(x)

    return res


def find_workingdir(executable):
    for check in get_possible_workingdirs(executable):
        full = os.path.join(check, 'etc', 'cluemapper', 'cluemapper.ini')
        if os.path.exists(full):
            return check

    return


def main(cmdargs=sys.argv[1:]):
    """Runs the server as a standalone server."""
    parser = optparse.OptionParser()
    parser.add_option('-d', '--debug', action='store_true', dest='debug', help='show all debug messages')
    parser.add_option('-p', '--pdb', action='store_true', dest='pdb', help='post mortem debugging')
    parser.add_option('-t', '--test-run', action='store_true', dest='test_run', help='test run')
    parser.add_option('-w', '--workingdir', action='store', dest='workingdir', help='working directory, this is where $workingdir/var/cluemapper and $workingdir/etc/cluemapper must live (ie specifying "/" would require /var/cluemapper to exist)')
    (options, args) = parser.parse_args(cmdargs)
    logger = utils.setup_logger()
    workingdir = options.workingdir
    if not workingdir:
        workingdir = find_workingdir(sys.argv[0])
    if not workingdir:
        workingdir = get_possible_workingdirs(sys.argv[0])[0]
    if options.debug:
        logger.setLevel(logging.DEBUG)
    server = Server(workingdir, options.pdb, logger=logger)
    if options.test_run:
        server._iter_count = 0
        server.logger.setLevel(logging.ERROR)
    server.serve_forever()
    return 0