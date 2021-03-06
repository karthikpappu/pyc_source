# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/futuregrid_move/utils/FGAuth.py
# Compiled at: 2012-07-09 15:56:59
"""
utility class for static methods
"""
__author__ = 'Fugang Wang'
import logging, sys, os, ConfigParser, hashlib, base64, binascii, ldap
from getpass import getpass
from futuregrid_move.utils.fgLog import fgLog
from futuregrid_move.utils.FGTypes import FGCredential
configFileName = 'fg-server.conf'
configFileNameClient = 'fg-client.conf'

def auth(userId, cred):
    ret = False
    testmode = False
    _localpath = '~/.fg/'
    _configfile = os.path.expanduser(_localpath) + '/' + configFileName
    _fgpath = ''
    try:
        _fgpath = os.environ['FG_PATH']
    except KeyError:
        _fgpath = os.path.dirname(os.path.abspath(__file__)) + '/../'

    if not os.path.isfile(_configfile):
        _configfile = '/etc/futuregrid/' + configFileName
        if not os.path.isfile(_configfile):
            print 'ERROR: configuration file ' + configFileName + ' not found'
            sys.exit(1)
    configFile = _configfile
    config = ConfigParser.ConfigParser()
    config.read(configFile)
    logfile = os.path.expanduser(config.get('LDAP', 'log'))
    try:
        testinput = eval(config.get('LDAP', 'test'))
        if testinput != False and testinput != True:
            testmode = False
        else:
            testmode = testinput
    except:
        testmode = False

    log = fgLog(logfile, logging.INFO, 'utils.FGAuth Auth', False)
    authProvider = cred.getProvider()
    authCred = cred.getCred()
    if authProvider == 'ldappass' or authProvider == 'ldappassmd5':
        if authCred != '':
            host = config.get('LDAP', 'LDAPHOST')
            adminuser = config.get('LDAP', 'LDAPUSER')
            adminpass = config.get('LDAP', 'LDAPPASS')
            userdn = 'uid=' + userId + ',ou=People,dc=futuregrid,dc=org'
            ldapconn = ldap.initialize('ldap://' + host)
            log.info('Initializing the LDAP connection to server: ' + host)
            try:
                try:
                    ldapconn.start_tls_s()
                    log.info('tls started...')
                    ldapconn.bind_s(adminuser, adminpass)
                    passwd_input = authCred
                    if authProvider == 'ldappass':
                        m = hashlib.md5()
                        m.update(authCred)
                        passwd_input = m.hexdigest()
                    passwd_processed = '{MD5}' + base64.b64encode(binascii.unhexlify(passwd_input))
                    if ldapconn.compare_s(userdn, 'userPassword', passwd_processed):
                        ret = True
                        log.info("User '" + userId + "' successfully authenticated")
                    else:
                        ret = False
                        log.info("User '" + userId + "' failed to authenticate due to incorrect credential")
                except ldap.INVALID_CREDENTIALS:
                    log.info('Your username or password is incorrect. Cannot bind as admin.')
                    ret = False
                except ldap.LDAPError:
                    log.info("User '" + userId + "' failed to authenticate due to LDAP error. The user may not exist." + str(sys.exc_info()))
                    ret = False
                except:
                    ret = False
                    log.info("User '" + userId + "' failed to authenticate due to possible password encryption error." + str(sys.exc_info()))

            finally:
                log.info('Unbinding from the LDAP.')
                ldapconn.unbind()

    elif authProvider == 'drupalplain':
        import MySQLdb
        if authCred != '':
            m = hashlib.md5()
            m.update(authCred)
            passwd_input = m.hexdigest()
            dbhost = config.get('PortalDB', 'host')
            dbuser = config.get('PortalDB', 'user')
            dbpasswd = config.get('PortalDB', 'passwd')
            dbname = config.get('PortalDB', 'db')
            conn = MySQLdb.connect(dbhost, dbuser, dbpasswd, dbname)
            cursor = conn.cursor()
            queryuser = "select pass from users where name='" + userId + "'"
            cursor.execute(queryuser)
            passwd_db = ''
            passwd = cursor.fetchall()
            for thepass in passwd:
                passwd_db = list(thepass)[0]

            if passwd_db != '' and passwd_db == passwd_input:
                ret = True
                log.info('User ' + userId + ' successfully authenticated')
            else:
                ret = False
                log.info('User ' + userId + ' failed to authenticate')
    if not testmode:
        return ret
    else:
        return True


def simpleauth(userId, cred):
    ret = False
    testmode = False
    _localpath = '~/.fg/'
    _configfile = os.path.expanduser(_localpath) + '/' + configFileNameClient
    _fgpath = ''
    try:
        _fgpath = os.environ['FG_PATH']
    except KeyError:
        _fgpath = os.path.dirname(os.path.abspath(__file__)) + '/../'

    if not os.path.isfile(_configfile):
        _configfile = '/etc/futuregrid/' + configFileNameClient
        if not os.path.isfile(_configfile):
            print 'ERROR: configuration file ' + configFileNameClient + ' not found'
            sys.exit(1)
    configFile = _configfile
    config = ConfigParser.ConfigParser()
    config.read(configFile)
    logfile = os.path.expanduser(os.path.expandvars(config.get('LDAP', 'log')))
    log = fgLog(logfile, logging.INFO, 'utils.FGAuth Auth', False)
    try:
        testinput = eval(config.get('LDAP', 'test'))
        if testinput != False and testinput != True:
            testmode = False
        else:
            testmode = testinput
    except:
        testmode = False

    authProvider = cred.getProvider()
    authCred = cred.getCred()
    if authProvider == 'ldappass':
        if authCred != '':
            host = config.get('LDAP', 'LDAPHOST')
            userdn = 'uid=' + userId + ',ou=People,dc=futuregrid,dc=org'
            ldapconn = ldap.initialize('ldap://' + host)
            log.info('Initializing the LDAP connection to server: ' + host)
            try:
                try:
                    ldapconn.start_tls_s()
                    log.info('tls started...')
                    ldapconn.bind_s(userdn, authCred)
                    ret = True
                except ldap.INVALID_CREDENTIALS:
                    log.info('Your username or password is incorrect. Cannot bind.')
                    ret = False
                except ldap.LDAPError:
                    log.info("User '" + userId + "' failed to authenticate due to LDAP error. The user may not exist." + str(sys.exc_info()))
                    ret = False
                except:
                    ret = False
                    log.info("User '" + userId + "' failed to authenticate due to possible password encryption error." + str(sys.exc_info()))

            finally:
                log.info('Unbinding from the LDAP.')
                ldapconn.unbind()

    if not testmode:
        return ret
    else:
        return True


if __name__ == '__main__':
    m = hashlib.md5()
    m.update(getpass())
    passwd_input = m.hexdigest()
    cred = FGCredential('ldappassmd5', passwd_input)
    if auth('jdiaz', cred):
        print 'logged in'
    else:
        print 'access denied'