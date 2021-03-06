# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/centinel/vpn/openvpn.py
# Compiled at: 2016-04-08 15:42:28
import logging, os, signal, subprocess, threading, time

class OpenVPN:
    connected_instances = []

    def __init__(self, config_file=None, auth_file=None, crt_file=None, tls_auth=None, key_direction=None, timeout=60):
        self.started = False
        self.stopped = False
        self.error = False
        self.notifications = ''
        self.auth_file = auth_file
        self.crt_file = crt_file
        self.tls_auth = tls_auth
        self.key_dir = key_direction
        self.config_file = config_file
        self.thread = threading.Thread(target=self._invoke_openvpn)
        self.thread.setDaemon(1)
        self.timeout = timeout

    def _invoke_openvpn(self):
        cmd = [
         'sudo', 'openvpn', '--script-security', '2']
        if self.config_file is not None:
            cmd.extend(['--config', self.config_file])
        if self.crt_file is not None:
            cmd.extend(['--ca', self.crt_file])
        if self.tls_auth is not None and self.key_dir is not None:
            cmd.extend(['--tls-auth', self.tls_auth, self.key_dir])
        if self.auth_file is not None:
            cmd.extend(['--auth-user-pass', self.auth_file])
        self.process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        self.kill_switch = self.process.terminate
        self.starting = True
        while True:
            line = self.process.stdout.readline().strip()
            if not line:
                break
            self.output_callback(line, self.process.terminate)

        return

    def output_callback(self, line, kill_switch):
        """Set status of openvpn according to what we process"""
        self.notifications += line + '\n'
        if 'Initialization Sequence Completed' in line:
            self.started = True
        if 'ERROR:' in line or 'Cannot resolve host address:' in line:
            self.error = True
        if 'process exiting' in line:
            self.stopped = True

    def start(self, timeout=None):
        """
        Start OpenVPN and block until the connection is opened or there is
        an error
        :param timeout: time in seconds to wait for process to start
        :return:
        """
        if not timeout:
            timeout = self.timeout
        self.thread.start()
        start_time = time.time()
        while start_time + timeout > time.time():
            self.thread.join(1)
            if self.error or self.started:
                break

        if self.started:
            logging.info('OpenVPN connected')
            OpenVPN.connected_instances.append(self)
        else:
            logging.warn('OpenVPN not started')
            for line in self.notifications.split('\n'):
                logging.warn('OpenVPN output:\t\t%s' % line)

    def stop(self, timeout=None):
        """
        Stop OpenVPN process group
        :param timeout: time in seconds to wait for process to stop
        :return:
        """
        if not timeout:
            timeout = self.timeout
        os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
        self.thread.join(timeout)
        if self.stopped:
            logging.info('OpenVPN stopped')
            if self in OpenVPN.connected_instances:
                OpenVPN.connected_instances.remove(self)
        else:
            logging.error('Cannot stop OpenVPN!')
            for line in self.notifications.split('\n'):
                logging.warn('OpenVPN output:\t\t%s' % line)