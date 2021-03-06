# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/pilight_python/pilight/test/pilight_daemon.py
# Compiled at: 2016-10-19 05:32:32
""" This is a helper class providing a pilight-daemon in python.

    This daemon just simulates the behavior of the real pilight-daemon
    and is used for testing only. Of cause only a few important
    commands are supported.

    This is a very hackish synchronous daemon that is
    not an example for good socket servers!
"""
import datetime, json, socket, threading, time, sys
if sys.version[0] == '2':
    import Queue as queue
else:
    import queue
HOST = '127.0.0.1'
PORT = 5000
SEND_DELAY = 0.1
FAKE_DATA = {'origin': 'receiver', 'repeats': 1, 
   'message': {'protocol': [
                          'kaku_switch'], 
               'id': 0, 
               'unit': 0, 
               'off': 1}}

class PilightDaemon(object):
    """Provide a pilight-daemon in with-statement."""

    def __init__(self, host=HOST, port=PORT, send_codes=False):
        self.host = host
        self.port = port
        self.send_codes = send_codes
        self.pilight_daemon = PilightDeamonSim(self.host, self.port, self.send_codes)

    def __enter__(self):
        self.pilight_daemon.start()
        time.sleep(0.1)
        return self.pilight_daemon

    def __exit__(self, _, value, traceback):
        self.pilight_daemon.stop()
        time.sleep(0.1)


class PilightDeamonSim(threading.Thread):
    """Simulate the pilight-daemon API for testing."""

    def __init__(self, host, port, send_codes):
        self.send_codes = send_codes
        threading.Thread.__init__(self)
        self.daemon = True
        self._stop_thread = threading.Event()
        self._lock = threading.Lock()
        self._data = queue.Queue()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        time.sleep(0.1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        time.sleep(0.1)
        self.server_socket.settimeout(0.01)
        for _ in range(10):
            try:
                self.server_socket.bind((host, port))
                break
            except socket.error:
                time.sleep(1)

        else:
            raise RuntimeError('Cannot create socket connection')

        self.server_socket.listen(2)
        self.client_sockets = []
        self.last_send = datetime.datetime.now()

    def run(self):
        """Simple infinite loop handling socket connections."""
        with self._lock:
            while not self._stop_thread.wait(0.01):
                self._handle_client_connections()
                self._handle_client_data()
                self._send_codes()

        for client_socket in self.client_sockets:
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()

    def _send_codes(self):
        if self.send_codes:
            if (datetime.datetime.now() - self.last_send).total_seconds() > SEND_DELAY:
                if len(self.client_sockets) > 0:
                    for i in range(10):
                        fake_data = FAKE_DATA.copy()
                        fake_data['repeats'] = i + 1
                        self.client_sockets[0].send(json.dumps(fake_data).encode())
                        time.sleep(0.01)

    def _handle_client_connections(self):

        def _new_client(client_socket):
            """Handle new client connection.

            Fake pilight-daemon protocol by returning success on identifiy action.
            """

            def _acknowledge_connection(messages):
                for message in messages:
                    if message:
                        message_dict = json.loads(message.decode())
                        if 'action' in message_dict:
                            if message_dict['action'] == 'identify':
                                client_socket.sendall(json.dumps({'status': 'success'}).encode())
                            else:
                                client_socket.sendall(json.dumps({'status': 'failure'}).encode())
                            break

            client_socket.settimeout(0.01)
            messages = client_socket.recv(1024).splitlines()
            _acknowledge_connection(messages)
            return client_socket

        try:
            self.client_sockets.append(_new_client(self.server_socket.accept()[0]))
        except socket.timeout:
            pass

    def _handle_client_data(self):

        def _handle_message(client_socket):
            """Called in poll loop to handle messages."""
            try:
                messages = client_socket.recv(1024).splitlines()
                for message in messages:
                    if message:
                        message_dict = json.loads(message.decode())
                        self._data.put(message_dict)
                        if message_dict['code']['protocol'] == 'daycom':
                            client_socket.sendall(json.dumps({'status': 'success'}).encode())
                        else:
                            client_socket.sendall(json.dumps({'status': 'failure'}).encode())

            except socket.error:
                pass

        for client_socket in self.client_sockets:
            try:
                _handle_message(client_socket)
            except socket.timeout:
                pass

    def get_data(self):
        """Return received data."""
        return self._data.get()

    def stop(self):
        """Called to stop the reveiver thread."""
        self._stop_thread.set()
        with self._lock:
            try:
                self.server_socket.shutdown(socket.SHUT_RDWR)
            except socket.error:
                pass

            self.server_socket.close()