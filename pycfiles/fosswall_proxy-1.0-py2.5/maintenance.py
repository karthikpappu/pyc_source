# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fosswallproxy0/maintenance.py
# Compiled at: 2008-02-14 01:30:06
from base import *
ENABLED = 0

class Maintenance(Base):

    @expose(template='fosswallproxy.templates.menu')
    def index(self):
        menu = dict(haproxy='Restart HAProxy', pound='Restart Pound')
        return dict(title='Maintenance', menu=menu)

    @expose()
    def haproxy(self):
        cmd = 'sudo /usr/local/sbin/haproxy -f /etc/haproxy/haproxy.cfg -p /var/run/haproxy.pid -sf $(cat /var/run/haproxy.pid) 2>&1'
        msg = 'Disabled HAProxy restart'
        if self.run(cmd):
            msg = 'Successfully restarted HAProxy'
        flash(msg)
        redirect('index')
        return msg

    @expose()
    def pound(self):
        cmd = 'sudo /etc/rc.d/init.d/pound restart'
        msg = 'Disabled Pound restart'
        if self.run(cmd):
            msg = 'Successfully restarted Pound'
        flash(msg)
        redirect('index')
        return msg

    def run(self, cmd):
        if ENABLED:
            send_stat = os.system(cmd)
            if send_stat == 0:
                return True
            else:
                raise Error('Error running %s' % cmd)
        else:
            return False