# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/cliresms.py
# Compiled at: 2014-12-21 09:54:45
from __future__ import print_function
import argparse
try:
    from http import cookiejar
except ImportError:
    import cookielib as cookiejar

import datetime, getpass, json, logging, os, re, signal, sys, time
try:
    from urllib.parse import urlencode
    from urllib.request import urlopen, build_opener, install_opener, Request, HTTPCookieProcessor
    from urllib.error import URLError, HTTPError
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, build_opener, install_opener, Request, HTTPCookieProcessor
    from urllib2 import URLError, HTTPError

try:
    raw_input
except NameError:
    raw_input = input

__version__ = '0.2.0'
__conf_file__ = os.path.join(os.path.expanduser('~'), '.cliresms.conf')
__cookie_file__ = os.path.join(os.path.expanduser('~'), '.cliresms.cookie')
log = logging.getLogger()
username = None
password = None
split = True
carrier = None
message = None
aliases = {}
recipients = []
conf_file = None
get_carriers = lambda : dict((cls.carrier_name(), cls) for cls in Account.__subclasses__())

def main():
    global carrier
    global conf_file
    global password
    global split
    global username
    signal.signal(signal.SIGINT, signal_handler)
    try:
        cli_parser = setup_parser()
        args = cli_parser.parse_args()
    except IOError as err:
        print(err)
        return err.errno

    loglevel = logging.WARN - args.verbose * 10
    logging.basicConfig(level=loglevel)
    if args.conf_file:
        conf_file = args.conf_file
    else:
        try:
            conf_file = open(__conf_file__, 'r+')
        except IOError as err:
            pass

    if conf_file:
        read_config(conf_file)
    if args.username:
        username = args.username
    elif not username:
        username = raw_input('Username: ').strip()
    if args.password:
        password = args.password
    elif not password:
        password = getpass.getpass()
    carrier_names = get_carriers().keys()
    if args.carrier:
        carrier = args.carrier
    else:
        if not carrier:
            carrier = raw_input('Carrier [%s]: ' % (', ').join(carrier_names)).strip()
        if carrier not in carrier_names:
            log.error('Invalid carrier. Specify one of: %s' % (', ').join(carrier_names))
            return 1
        if not split and args.split_messages:
            split = True
        try:
            process_recipients(args.recipients)
        except ValueError:
            return 1

        message = get_message(args.message)
        while True:
            try:
                send_message(recipients, message)
                break
            except (HTTPError, URLError, LoginException) as e:
                e.message = {HTTPError: 'Server could not fulfill the request.', URLError: 'Server unreachable.'}.get(type(e), e.message)
                log.error(e.message)
                choice = raw_input('Retry send? [Y/n] ').lower()
                if choice in ('y', ''):
                    continue
                else:
                    break

    save_aliases()


def read_config(file):
    global carrier
    global password
    global split
    global username
    for line in map(lambda s: s.strip(), file.readlines()):
        if not line or line.startswith('#'):
            continue
        log.debug('Parsing line: %s', repr(line))
        if 'username' in line:
            username = line.split()[(-1)]
        elif 'password' in line:
            password = line.split()[(-1)]
        elif 'carrier' in line:
            carrier = line.split()[(-1)]
        elif 'nosplit' in line:
            split = False
        elif 'alias' in line:
            try:
                pattern = '^\\s*alias\\s+([\\w\\.\\-\\_]+)\\s+([\\w\\s\\+\\.-]+)\\s*'
                matches = re.search(pattern, line)
                alias_name = matches.group(1)
                alias_contacts = re.sub('[\\.-]', '', matches.group(2).strip())
                alias_contacts = re.findall('(\\+?\\d+|\\w+)', alias_contacts)
                alias_numbers = []
                for contact in alias_contacts:
                    if re.search('^\\+?\\d+$', contact):
                        number = contact
                        alias_numbers.append(number)
                    else:
                        try:
                            log.debug("Looking for entry: '%s'", contact)
                            number_list = aliases[contact]
                            alias_numbers.extend(number_list)
                        except KeyError:
                            log.exception('Could not find %s, if you define aliases, you need to defined the referenced numbers first', name_or_number)
                            log.info('So far, the known aliases are: %s', aliases)
                            raise

                log.debug('Defining %s as %s', alias_name, alias_numbers)
                aliases[alias_name] = alias_numbers
            except AttributeError:
                log.exception('Problem parsing line:\n%s', line)
                raise

        else:
            log.error('Could not parse line:\n%s', line)


def get_message(message=None):
    if not message:
        print('Enter your message:')
        input = []
        while True:
            try:
                line = raw_input()
                if '.' == line:
                    break
            except EOFError:
                break

            input.append(line)

        message = ('\n').join(input)
    return message


def split_message(message, length=160):
    if len(message) > length:
        if split:
            messages = [ message[i:i + length].strip() for i in range(0, len(message), length)
                       ]
            print('Message length %d (%d max) will be sent in %d texts' % (
             len(message), length, len(messages)))
        else:
            log.warning('Message is %d chars, sending only first %d chars', len(message), length)
            messages = [message[:length]]
    else:
        messages = [
         message[:length]]
    message_length = sum([ len(message) for message in messages ])
    log.info('Messages (%d chars): %s', message_length, messages)
    return messages


def process_recipients(arg_recipients):
    """Return a list of only numbers from alias definitions and any numbers entered"""
    for recipient in arg_recipients:
        if recipient in aliases:
            recipients.extend(aliases[recipient])
        elif re.search('\\+?\\d', recipient):
            recipients.append(recipient)
        else:
            log.error('Alias %s unknown', recipient)
            log.error('Known aliases: %s', (', ').join(sorted(aliases.keys(), key=lambda x: x.lower())))
            raise ValueError('Unknown alias: %s' % recipient)


def save_aliases():
    if not conf_file:
        return
    new_aliases = {}
    alias_nums = [ num for sublist in aliases.values() for num in sublist ]
    for num in recipients:
        if num in alias_nums:
            continue
        while True:
            entered = raw_input('Create alias for %s with this name: ' % num).strip()
            if len(entered) < 1:
                break
            if not entered.isalpha():
                print('%s is an invalid alias name, no numbers allowed' % entered)
                continue
            if entered in aliases:
                print('alias already exists')
                continue
            new_aliases[entered] = num
            break

    for name in new_aliases:
        try:
            conf_file.write('alias %s %s\n' % (name, new_aliases[name]))
        except:
            print('Could not write aliases to configuration file %s' % os.path.abspath(f.name))


def send_message(recipients, message):
    account_type = get_carriers().get(carrier)
    if not account_type:
        log.error('Invalid carrier. Qutting...')
        return
    account = account_type(username, password)
    recipients_validated = []
    for recipient in recipients:
        try:
            recipients_validated.append(account.validate_number(recipient))
        except ValueError as err:
            log.warning(err)
            recipients.remove(recipient)

    if account.login():
        print('Logged in')
    else:
        raise LoginException('Could not login.')
    if account.texts_remaining == 0:
        raise LoginException("You don't have any more texts remaining.")
    else:
        if account.texts_remaining < 0:
            raise LoginException('Could not determine number of texts remaining.')
        print('Sending message...', end='')
        sys.stdout.flush()
        for message_part in split_message(message, account.message_length):
            if account.send_message(recipients_validated, message_part):
                account.texts_remaining -= len(recipients_validated)
                print('Message sent, %s texts remaining.' % account.texts_remaining)


def setup_parser():
    parser = argparse.ArgumentParser(prog='cliresms', description='Send webtexts from the command line')
    parser.add_argument('recipients', metavar='<number|alias|group>', nargs='+', help='One or more numbers or entries in the config file')
    parser.add_argument('-u', '--username', metavar='STRING', help='Use this username (defaults to unix username)')
    parser.add_argument('-p', '--password', metavar='STRING', help='Use this password (if omitted, will prompt for password)')
    parser.add_argument('-c', '--config', metavar='FILE', type=argparse.FileType('r+'), dest='conf_file', help='Use this configuration file (defaults to ~/.cliresms.conf)')
    parser.add_argument('-s', '--split-messages', action='store_true', help='Allow message to be split into multiple SMSs (the default, overrides config file nosplit)')
    parser.add_argument('-C', '--carrier', metavar='NAME', help="Force the carrier to be this (``meteor'', ``o2'' or ``three''")
    parser.add_argument('-m', '--message', metavar='STRING', help="Don't wait for STDIN, send this message")
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    return parser


def signal_handler(signum, frame):
    print("\nokay, I'm outta here...")
    sys.exit(1)


class Account(object):
    message_length = 480

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cj = cookiejar.MozillaCookieJar(__cookie_file__)
        self._texts_remaining = None
        opener = build_opener(HTTPCookieProcessor(self.cj))
        install_opener(opener)
        return

    def login(self, request=None):
        print('Logging in...', end='')
        sys.stdout.flush()
        if os.path.isfile(__cookie_file__):
            try:
                self.cj.load()
            except cookiejar.LoadError:
                log.exception('Error loading cookie file, try to delete %s', __cookie_file__)
                raise

            for c in self.cj:
                if c.name in self.cookies['session']:
                    print('(using existing session)', end=' ')
                    sys.stdout.flush()
                    return True

        if request:
            response = urlopen(request)
        else:
            data = urlencode(self.login_form_data).encode('utf-8')
            response = urlopen(self.login_url, data)
        if self.loggedin_url in response.geturl():
            self.save_cookies()
            return True

    def save_cookies(self):
        for c in self.cj:
            if c.name == self.cookies['session']:
                login_cookie = c

        login_cookie.discard = False
        future = datetime.datetime.now() + datetime.timedelta(minutes=30)
        unix_time = int(time.mktime(future.timetuple()))
        login_cookie.expires = unix_time
        self.cj.save()

    def validate_number(self, recipient):
        recipient = re.sub('[\\s\\-\\.]', '', recipient)
        if re.search('[^\\d\\+]', recipient):
            raise ValueError('Number contains invalid characters. Only a + and                     digits are allowed.')
        return recipient

    @property
    def texts_remaining(self):
        if not self._texts_remaining:
            self._texts_remaining = self._get_texts_remaining()
        return self._texts_remaining

    @texts_remaining.setter
    def texts_remaining(self, value):
        self._texts_remaining = value

    @classmethod
    def carrier_name(cls):
        match = re.match('(\\w+)Account', cls.__name__)
        if match:
            return match.group(1).lower()


class MeteorAccount(Account):

    def __init__(self, username, password):
        super(MeteorAccount, self).__init__(username, password)
        self.cookies = {'login': 'MyMeteorCMS-cookie', 'session': 'JSESSIONID'}
        self.login_url = 'https://www.mymeteor.ie/go/mymeteor-login-manager'
        self.loggedin_url = 'https://www.mymeteor.ie/postpaylanding'
        self.login_form_data = {'username': self.username, 'userpass': self.password, 
           'login': '', 
           'returnTo': '/'}

    def _get_texts_remaining(self):
        url = 'https://www.mymeteor.ie/go/freewebtext'
        pat = 'Free web texts left <input type="text" id="numfreesmstext" value="(\\d+)" disabled size=2>'
        response = urlopen(url)
        response_data = response.read().decode('utf-8')
        match = re.search(pat, response_data)
        log.debug('Texts remaining page:\n%s', response_data)
        self.texts_remaining = int(match.group(1) if match else -1)
        return self.texts_remaining

    def validate_number(self, recipient):
        recipient = super(MeteorAccount, self).validate_number(recipient)
        recipient = re.sub('(\\+353|00353)', '0', recipient)
        if re.search('^08[0-9]\\d{7}', recipient):
            return recipient
        raise ValueError('%s is invalid; expected 10 digits beginning with 08' % recipient)

    def send_message(self, recipients, message):
        url = 'https://www.mymeteor.ie/mymeteorapi/index.cfm'
        pat = 'showEl\\("sentTrue"\\)'
        for recipient in recipients:
            data = {'event': 'smsAjax', 'func': 'addEnteredMsisdns', 
               'ajaxRequest': 'addEnteredMSISDNs', 
               'remove': '-', 
               'add': '0|' + recipient}
            params = urlencode(data)
            urlopen(url + '?' + params)

        data = {'event': 'smsAjax', 'func': 'sendSMS', 
           'ajaxRequest': 'sendSMS', 
           'messageText': message}
        params = urlencode(data)
        response = urlopen(url + '?' + params)
        if re.search(pat, response.read().decode('utf-8')):
            return True


class ThreeAccount(Account):

    def __init__(self, username, password):
        super(ThreeAccount, self).__init__(username, password)
        self.cookies = {'login': 'CAKEPHP', 'session': 'AWSELB'}
        self.login_url = 'https://webtexts.three.ie/webtext/users/login'
        self.loggedin_url = 'https://webtexts.three.ie/webtext/messages/send'
        self.login_form_data = {'data[User][telephoneNo]': self.username, 'data[User][pin]': self.password}

    def _get_texts_remaining(self):
        url = self.loggedin_url
        pat = 'Remaining texts\\D*(\\d+) \\(of (\\d+)\\)'
        response = urlopen(url)
        match = re.search(pat, response.read().decode('utf-8'))
        self.texts_remaining = int(match.group(1) if match else -1)
        return self.texts_remaining

    def send_message(self, recipients, message):
        url = self.loggedin_url
        pat = 'Message sent'
        data = {'data[Message][message]': message, 'data[Message][recipients_individual]': (', ').join(recipients)}
        data = urlencode(data).encode('utf-8')
        response = urlopen(url, data)
        if re.search(pat, response.read().decode('utf-8')):
            return True

    def save_cookies(self):
        for c in self.cj:
            if c.name == self.cookies['login']:
                login_cookie = c
            if c.name == self.cookies['session']:
                session_cookie = c

        session_cookie.discard = False
        session_cookie.expires = login_cookie.expires
        self.cj.save()


class O2Account(Account):

    def __init__(self, username, account):
        super(O2Account, self).__init__(username, password)
        self.cookies = {'session': 'iPlanetDirectoryPro'}
        self.login_url = 'https://www.o2online.ie/amserver/UI/Login'
        self.loggedin_url = 'http://www.o2online.ie/wps/wcm/connect/O2/Logged+in/LoginCheck'
        self.login_form_data = {'org': 'o2ext', 'IDButton': 'Go', 
           'org': 'o2ext', 
           'CONNECTFORMGET': 'TRUE', 
           'IDToken1': self.username, 
           'IDToken2': self.password}

    def login(self):
        data = urlencode(self.login_form_data).encode('utf-8')
        request = Request(self.login_url, data)
        request.add_header('Referer', self.loggedin_url)
        if Account.login(self, request):
            return self.find_sid()

    def find_sid(self):
        url = 'http://messaging.o2online.ie/ssomanager.osp?APIID=AUTH-WEBSSO&TargetApp=o2om_smscenter_new.osp%3FMsgContentID%3D-1%26SID%3D_'
        pat = 'o2om_smscenter_new.osp\\?MsgContentID=-1&SID=_&SID=(\\w+)'
        response = urlopen(url)
        match = re.search(pat, response.read().decode('utf-8'))
        if match:
            self.sid = match.group(1)
            return True

    def _get_texts_remaining(self):
        url = 'http://messaging.o2online.ie/smscenter_evaluate.osp'
        data = {'SID': self.sid, 'SMSText': 'text', 
           'FID': '6406'}
        data = urlencode(data).encode('utf-8')
        request = Request(url, data)
        request.add_header('Referer', request.get_origin_req_host())
        response = urlopen(request)
        try:
            content = self.parse_json(response.read().decode('utf-8'))
        except ValueError:
            content = None

        self.texts_remaining = content['freeMessageCount'] if content else -1
        return self.texts_remaining

    def send_message(self, recipients, message):
        url = 'http://messaging.o2online.ie/smscenter_send.osp'
        data = {'SID': self.sid, 'MsgContentID': '-1', 
           'SMSTo': (', ').join(recipient), 
           'SMSText': message}
        data = urlencode(data).encode('utf-8')
        request = Request(url, data)
        request.add_header('Referer', request.get_origin_req_host())
        response = urlopen(request)
        content = self.parse_json(response.read().decode('utf-8'))
        return content['isSuccess']

    def parse_json(self, content):
        comment_re = re.compile('(^)?[^\\S\n]*/(?:\\*(.*?)\\*/[^\\S\n]*|/[^\n]*)($)?', re.DOTALL | re.MULTILINE)
        match = comment_re.search(content)
        while match:
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)

        content = re.sub("'", '"', content)
        content = re.sub(' \\* \\d*,', ',', content)

        def quote_wrap(match):
            offset = match.start()
            beginning = match.group()[match.start() - offset:match.start(1) - offset]
            ending = match.group()[match.start(1) - offset + len(match.group(1)):]
            return beginning + '"' + match.group(1) + '"' + ending

        quote_re = re.compile('[{,][\\n\\r\\t]*\\s*(\\w+)\\s*:')
        return json.loads(quote_re.sub(quote_wrap, content))


class LoginException(Exception):
    pass


if __name__ == '__main__':
    sys.exit(main())