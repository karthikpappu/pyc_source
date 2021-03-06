# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bart/libobj/mods/email.py
# Compiled at: 2020-03-03 07:58:36
# Size of source mod 2**32: 3539 bytes
import lo, mailbox, os, random
bdmonths = [
 'Bo', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
 'Sep', 'Oct', 'Nov', 'Dec']
monthint = {'Jan':1, 
 'Feb':2, 
 'Mar':3, 
 'Apr':4, 
 'May':5, 
 'Jun':6, 
 'Jul':7, 
 'Aug':8, 
 'Sep':9, 
 'Oct':10, 
 'Nov':11, 
 'Dec':12}

class Email(lo.Object):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.text = ''


def to_date(date):
    date = date.replace('_', ':')
    res = date.split()
    ddd = ''
    try:
        if '+' in res[3]:
            raise ValueError
        if '-' in res[3]:
            raise ValueError
        int(res[3])
        ddd = '{:4}-{:#02}-{:#02} {:6}'.format(res[3], monthint[res[2]], int(res[1]), res[4])
    except (IndexError, KeyError, ValueError):
        try:
            if '+' in res[4]:
                raise ValueError
            if '-' in res[4]:
                raise ValueError
            int(res[4])
            ddd = '{:4}-{:#02}-{:02} {:6}'.format(res[4], monthint[res[1]], int(res[2]), res[3])
        except (IndexError, KeyError, ValueError):
            try:
                ddd = '{:4}-{:#02}-{:02} {:6}'.format(res[2], monthint[res[1]], int(res[0]), res[3])
            except (IndexError, KeyError):
                try:
                    ddd = '{:4}-{:#02}-{:02}'.format(res[2], monthint[res[1]], int(res[0]))
                except (IndexError, KeyError):
                    try:
                        ddd = '{:4}-{:#02}'.format(res[2], monthint[res[1]])
                    except (IndexError, KeyError):
                        try:
                            ddd = '{:4}'.format(res[2])
                        except (IndexError, KeyError):
                            ddd = ''

    return ddd


def cor(event):
    if not event.args:
        event.reply('cor <email>')
        return
    selector = lo.Object()
    selector.From = event.args[0]
    nr = 0
    db = lo.Db()
    for email in db.all('mods.Email', selector):
        event.reply('%s %s' % (nr, lo.gnr.format(email, selector.keys())))
        nr += 1


def email(event):
    if not event.args:
        event.reply('email <match>')
        return
    match = event.args[0]
    try:
        match, *args = event.args
    except ValueError:
        match = event.args[0]
        args = []

    nr = -1
    db = lo.Db()
    for o in db.find_value('mods.email.Email', match):
        nr += 1
        event.display(o, str(nr), args)


def mbox(event):
    if not event.args:
        event.reply('mbox <path>')
        return
    else:
        fn = os.path.expanduser(event.args[0])
        event.reply('reading from %s' % fn)
        nr = 0
        if os.path.isdir(fn):
            thing = mailbox.Maildir(fn, create=False)
        else:
            if os.path.isfile(fn):
                thing = mailbox.mbox(fn, create=False)
            else:
                event.reply('need a mbox or maildir.')
                return
    try:
        thing.lock()
    except FileNotFoundError:
        pass

    for m in thing:
        o = Email()
        o.update(m)
        try:
            sdate = os.sep.join(to_date(o.Date).split())
        except AttributeError:
            sdate = None

        o.text = ''
        for payload in m.walk():
            if payload.get_content_type() == 'text/plain':
                o.text += payload.get_payload()

        o.text = o.text.replace('\\n', '\n')
        o.save(stime=sdate)
        nr += 1

    if nr:
        event.reply('ok %s' % nr)