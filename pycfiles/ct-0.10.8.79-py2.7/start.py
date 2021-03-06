# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/scripts/start.py
# Compiled at: 2019-08-05 00:35:42
"""
### Usage: ctstart [--web_backend=BACKEND] [--port=PORT] [--datastore=DS_PATH]

### Options:
    -h, --help            show this help message and exit
    -w WEB_BACKEND, --web_backend=WEB_BACKEND
                          web backend. options: dez, gae. (default: dez)
    -p PORT, --port=PORT  select your port (default=8080)
    -a ADMIN_PORT, --admin_port=ADMIN_PORT
                          select your port (default=8002)
    -d DATASTORE, --datastore=DATASTORE
                          select your datastore file (default=sqlite:///data.db)
    -o, --overwrite_password
                          overwrite admin password (default=False)
"""
from optparse import OptionParser
from cantools import config
from cantools.util import error

def go():
    parser = OptionParser('ctstart [--web_backend=BACKEND] [--port=PORT] [--datastore=DS_PATH]')
    parser.add_option('-w', '--web_backend', dest='web_backend', default=config.web.server, help='web backend. options: dez, gae. (default: %s)' % (config.web.server,))
    parser.add_option('-p', '--port', dest='port', default=config.web.port, help='select your port (default=%s)' % (config.web.port,))
    parser.add_option('-a', '--admin_port', dest='admin_port', default=config.admin.port, help='select your port (default=%s)' % (config.admin.port,))
    parser.add_option('-d', '--datastore', dest='datastore', default=config.db.main, help='select your datastore file (default=%s)' % (config.db.main,))
    parser.add_option('-o', '--overwrite_password', action='store_true', dest='overwrite_password', default=False, help='overwrite admin password (default=False)')
    options, args = parser.parse_args()
    config.web.update('port', int(options.port))
    config.admin.update('port', int(options.admin_port))
    if options.overwrite_password:
        config.update('newpass', True)
    if options.web_backend == 'gae':
        import subprocess
        cmd = 'dev_appserver.py . --host=%s --port=%s --admin_port=%s --datastore_path=%s' % (config.web.host,
         options.port, options.admin_port, options.datastore)
        print cmd
        subprocess.call(cmd, shell=True)
    elif options.web_backend == 'dez':
        from cantools.web import run_dez_webserver
        run_dez_webserver()
    else:
        error('invalid web_backend: %s' % (options.web_backend,))


if __name__ == '__main__':
    go()