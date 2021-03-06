# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/web/dez_server/mail.py
# Compiled at: 2020-03-18 01:36:48
import rel, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..util import config, log, strip_html
TMP = 'From: %s\nTo: %s\nSubject: %s\n\n%s'

class Mailer(object):

    def __init__(self, addr, mailername):
        self.addr = addr
        self.name = mailername
        self._yag = None
        self._smtp = None
        self.queue = []
        self.churning = False
        if not addr:
            log('no email address configured')
        elif 'gmail.com' in addr:
            import yagmail
            if self.name:
                mailer = {}
                mailer[self.addr] = self.name
            else:
                mailer = self.addr.split('@')[0]
            try:
                self._yag = yagmail.SMTP(mailer, config.cache('email password? '))
            except:
                self._yag = yagmail.SMTP(mailer, config.cache('email password? ', overwrite=True))

        else:
            self._smtp = smtplib.SMTP('localhost')
        return

    def _refresh(self):
        log('refreshing smtp connection')
        if self._yag:
            self._yag.login(config.cache('email password? '))
            self._yag.send_unsent()
        elif self._smtp:
            self._smtp = smtplib.SMTP('localhost')

    def _noop(self):
        if self._yag and self._yag.is_closed or self._smtp and self._smtp.noop()[0] != 250:
            self._refresh()

    def _prep(self, *args):
        if str == bytes:
            return [ a and type(a) == unicode and a.encode('utf-8') or a for a in args ]
        return args

    def _body(self, sender, to, subject, body):
        if config.mailhtml:
            mpmsg = MIMEMultipart('alternative')
            mpmsg['Subject'] = subject
            mpmsg['From'] = sender
            mpmsg['To'] = to
            mpmsg.attach(MIMEText(strip_html(body), 'plain'))
            mpmsg.attach(MIMEText(body.replace('\n', '<br>'), 'html'))
            return mpmsg.as_string()
        else:
            return TMP % (sender, to, subject, body)

    def _emit(self, to, subject, body, bcc):
        log('emailing "%s" to %s' % (subject, to))
        if self._yag:
            self._yag.send(to, subject, body, bcc=bcc)
            if self._yag.unsent:
                self._refresh()
        elif self._smtp:
            sender = self.name and '%s <%s>' % (self.name, self.addr) or self.addr
            self._smtp.sendmail(self.addr, to, self._body(sender, to, subject, body))

    def _sender(self):
        while len(self.queue):
            to, subject, body, bcc = self.queue.pop(0)
            self._noop()
            self._emit(to, subject, body, bcc)

        log('closing mail thread')
        self.churning = False

    def _send(self, to, subject, body, bcc):
        log('enqueueing email "%s" to %s' % (subject, to))
        self.queue.append([to, subject, body, bcc])
        if not self.churning:
            log('spawning mail thread')
            self.churning = True
            rel.thread(self._sender)

    def mail(self, to=None, sender=None, subject=None, body=None, html=None, bcc=None):
        if not self._yag and not self._smtp:
            log('email attempted to "%s"' % (to,))
            log('## content start ##')
            log(body)
            log('## content end ##')
            return log('failed to send email -- no MAILER specified in ct.cfg!')
        to, subject, body, html = self._prep(to, subject, body, html)
        self._send(to, subject, html or body, bcc)

    def admins(self, subject, body):
        log('emailing admins: %s' % (subject,), important=True)
        log(body)
        for admin in config.admin.contacts:
            self.mail(to=admin, subject=subject, body=body)


mailer = Mailer(config.mailer, config.mailername)
send_mail = mailer.mail
email_admins = mailer.admins