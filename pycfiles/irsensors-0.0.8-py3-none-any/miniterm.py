# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/tools/miniterm.py
# Compiled at: 2015-09-30 10:49:43
import codecs, os, sys, threading, serial
from serial.tools.list_ports import comports
from serial.tools import hexlify_codec
codecs.register(lambda c: hexlify_codec.getregentry() if c == 'hexlify' else None)
try:
    raw_input
except NameError:
    raw_input = input
    unichr = chr

def key_description(character):
    """generate a readable description for a key"""
    ascii_code = ord(character)
    if ascii_code < 32:
        return 'Ctrl+%c' % (ord('@') + ascii_code)
    else:
        return repr(character)


class ConsoleBase(object):

    def __init__(self):
        if sys.version_info >= (3, 0):
            self.byte_output = sys.stdout.buffer
        else:
            self.byte_output = sys.stdout
        self.output = sys.stdout

    def setup(self):
        pass

    def cleanup(self):
        pass

    def getkey(self):
        return

    def write_bytes(self, s):
        self.byte_output.write(s)
        self.byte_output.flush()

    def write(self, s):
        self.output.write(s)
        self.output.flush()

    def __enter__(self):
        self.cleanup()
        return self

    def __exit__(self, *args, **kwargs):
        self.setup()


if os.name == 'nt':
    import msvcrt, ctypes

    class Out(object):

        def __init__(self, fd):
            self.fd = fd

        def flush(self):
            pass

        def write(self, s):
            os.write(self.fd, s)


    class Console(ConsoleBase):

        def __init__(self):
            super(Console, self).__init__()
            self._saved_ocp = ctypes.windll.kernel32.GetConsoleOutputCP()
            self._saved_icp = ctypes.windll.kernel32.GetConsoleCP()
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
            ctypes.windll.kernel32.SetConsoleCP(65001)
            self.output = codecs.getwriter('UTF-8')(Out(sys.stdout.fileno()), 'replace')
            sys.stderr = codecs.getwriter('UTF-8')(Out(sys.stderr.fileno()), 'replace')
            sys.stdout = self.output
            self.output.encoding = 'UTF-8'

        def __del__(self):
            ctypes.windll.kernel32.SetConsoleOutputCP(self._saved_ocp)
            ctypes.windll.kernel32.SetConsoleCP(self._saved_icp)

        def getkey(self):
            while True:
                z = msvcrt.getwch()
                if z == unichr(13):
                    return unichr(10)
                if z in (unichr(0), unichr(14)):
                    msvcrt.getwch()
                else:
                    return z


elif os.name == 'posix':
    import atexit, termios

    class Console(ConsoleBase):

        def __init__(self):
            super(Console, self).__init__()
            self.fd = sys.stdin.fileno()
            self.old = termios.tcgetattr(self.fd)
            atexit.register(self.cleanup)
            if sys.version_info < (3, 0):
                self.enc_stdin = codecs.getreader(sys.stdin.encoding)(sys.stdin)
            else:
                self.enc_stdin = sys.stdin

        def setup(self):
            new = termios.tcgetattr(self.fd)
            new[3] = new[3] & ~termios.ICANON & ~termios.ECHO & ~termios.ISIG
            new[6][termios.VMIN] = 1
            new[6][termios.VTIME] = 0
            termios.tcsetattr(self.fd, termios.TCSANOW, new)

        def getkey(self):
            c = self.enc_stdin.read(1)
            if c == unichr(127):
                c = unichr(8)
            return c

        def cleanup(self):
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old)


else:
    raise NotImplementedError('Sorry no implementation for your platform (%s) available.' % sys.platform)

class Transform(object):
    """do-nothing: forward all data unchanged"""

    def rx(self, text):
        """text received from serial port"""
        return text

    def tx(self, text):
        """text to be sent to serial port"""
        return text

    def echo(self, text):
        """text to be sent but displayed on console"""
        return text


class CRLF(Transform):
    """ENTER sends CR+LF"""

    def tx(self, text):
        return text.replace('\n', '\r\n')


class CR(Transform):
    """ENTER sends CR"""

    def rx(self, text):
        return text.replace('\r', '\n')

    def tx(self, text):
        return text.replace('\n', '\r')


class LF(Transform):
    """ENTER sends LF"""
    pass


class NoTerminal(Transform):
    """remove typical terminal control codes from input"""
    REPLACEMENT_MAP = dict((x, 9216 + x) for x in range(32) if unichr(x) not in '\r\n\x08\t')
    REPLACEMENT_MAP.update({127: 9249, 
       155: 9253})

    def rx(self, text):
        return text.translate(self.REPLACEMENT_MAP)

    echo = rx


class NoControls(NoTerminal):
    """Remove all control codes, incl. CR+LF"""
    REPLACEMENT_MAP = dict((x, 9216 + x) for x in range(32))
    REPLACEMENT_MAP.update({32: 9251, 
       127: 9249, 
       155: 9253})


class Printable(Transform):
    """Show decimal code for all non-ASCII characters and replace most control codes"""

    def rx(self, text):
        r = []
        for t in text:
            if ' ' <= t < '\x7f' or t in '\r\n\x08\t':
                r.append(t)
            elif t < ' ':
                r.append(unichr(9216 + ord(t)))
            else:
                r.extend(unichr(8320 + ord(d) - 48) for d in ('{:d}').format(ord(t)))
                r.append(' ')

        return ('').join(r)

    echo = rx


class Colorize(Transform):
    """Apply different colors for received and echo"""

    def __init__(self):
        self.input_color = '\x1b[37m'
        self.echo_color = '\x1b[31m'

    def rx(self, text):
        return self.input_color + text

    def echo(self, text):
        return self.echo_color + text


class DebugIO(Transform):
    """Print what is sent and received"""

    def rx(self, text):
        sys.stderr.write((' [RX:{}] ').format(repr(text)))
        sys.stderr.flush()
        return text

    def tx(self, text):
        sys.stderr.write((' [TX:{}] ').format(repr(text)))
        sys.stderr.flush()
        return text


EOL_TRANSFORMATIONS = {'crlf': CRLF, 
   'cr': CR, 
   'lf': LF}
TRANSFORMATIONS = {'direct': Transform, 
   'default': NoTerminal, 
   'nocontrol': NoControls, 
   'printable': Printable, 
   'colorize': Colorize, 
   'debug': DebugIO}

def ask_for_port():
    """    Show a list of ports and ask the user for a choice. To make selection
    easier on systems with long device names, also allow the input of an
    index.
    """
    sys.stderr.write('\n--- Available ports:\n')
    ports = []
    for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
        sys.stderr.write(('--- {:2}: {:20} {}\n').format(n, port, desc))
        ports.append(port)

    while True:
        port = raw_input('--- Enter port index or full name: ')
        try:
            index = int(port) - 1
            if not 0 <= index < len(ports):
                sys.stderr.write('--- Invalid index!\n')
                continue
        except ValueError:
            pass
        else:
            port = ports[index]

        return port


class Miniterm(object):
    """    Terminal application. Copy data from serial port to console and vice versa.
    Handle special keys from the console to show menu etc.
    """

    def __init__(self, serial_instance, echo=False, eol='crlf', filters=()):
        self.console = Console()
        self.serial = serial_instance
        self.echo = echo
        self.raw = False
        self.input_encoding = 'UTF-8'
        self.output_encoding = 'UTF-8'
        self.eol = eol
        self.filters = filters
        self.update_transformations()
        self.exit_character = 29
        self.menu_character = 20

    def _start_reader(self):
        """Start reader thread"""
        self._reader_alive = True
        self.receiver_thread = threading.Thread(target=self.reader, name='rx')
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

    def _stop_reader(self):
        """Stop reader thread only, wait for clean exit of thread"""
        self._reader_alive = False
        self.receiver_thread.join()

    def start(self):
        self.alive = True
        self._start_reader()
        self.transmitter_thread = threading.Thread(target=self.writer, name='tx')
        self.transmitter_thread.daemon = True
        self.transmitter_thread.start()
        self.console.setup()

    def stop(self):
        self.alive = False

    def join(self, transmit_only=False):
        self.transmitter_thread.join()
        if not transmit_only:
            self.receiver_thread.join()

    def update_transformations(self):
        transformations = [EOL_TRANSFORMATIONS[self.eol]] + [ TRANSFORMATIONS[f] for f in self.filters ]
        self.tx_transformations = [ t() for t in transformations ]
        self.rx_transformations = list(reversed(self.tx_transformations))

    def set_rx_encoding(self, encoding, errors='replace'):
        self.input_encoding = encoding
        self.rx_decoder = codecs.getincrementaldecoder(encoding)(errors)

    def set_tx_encoding(self, encoding, errors='replace'):
        self.output_encoding = encoding
        self.tx_encoder = codecs.getincrementalencoder(encoding)(errors)

    def dump_port_settings(self):
        sys.stderr.write(('\n--- Settings: {p.name}  {p.baudrate},{p.bytesize},{p.parity},{p.stopbits}\n').format(p=self.serial))
        sys.stderr.write(('--- RTS: {:8}  DTR: {:8}  BREAK: {:8}\n').format('active' if self.serial.rts else 'inactive', 'active' if self.serial.dtr else 'inactive', 'active' if self.serial.break_condition else 'inactive'))
        try:
            sys.stderr.write(('--- CTS: {:8}  DSR: {:8}  RI: {:8}  CD: {:8}\n').format('active' if self.serial.cts else 'inactive', 'active' if self.serial.dsr else 'inactive', 'active' if self.serial.ri else 'inactive', 'active' if self.serial.cd else 'inactive'))
        except serial.SerialException:
            pass

        sys.stderr.write(('--- software flow control: {}\n').format('active' if self.serial.xonxoff else 'inactive'))
        sys.stderr.write(('--- hardware flow control: {}\n').format('active' if self.serial.rtscts else 'inactive'))
        sys.stderr.write(('--- serial input encoding: {}\n').format(self.input_encoding))
        sys.stderr.write(('--- serial output encoding: {}\n').format(self.output_encoding))
        sys.stderr.write(('--- EOL: {}\n').format(self.eol.upper()))
        sys.stderr.write(('--- filters: {}\n').format((' ').join(self.filters)))

    def reader(self):
        """loop and copy serial->console"""
        try:
            while self.alive and self._reader_alive:
                data = self.serial.read(self.serial.in_waiting or 1)
                if data:
                    if self.raw:
                        self.console.write_bytes(data)
                    else:
                        text = self.rx_decoder.decode(data)
                        for transformation in self.rx_transformations:
                            text = transformation.rx(text)

                        self.console.write(text)

        except serial.SerialException:
            self.alive = False
            raise

    def writer(self):
        """        Loop and copy console->serial until self.exit_character character is
        found. When self.menu_character is found, interpret the next key
        locally.
        """
        menu_active = False
        try:
            while self.alive:
                try:
                    c = self.console.getkey()
                except KeyboardInterrupt:
                    c = '\x03'

                if menu_active:
                    self.handle_menu_key(c)
                    menu_active = False
                elif c == self.menu_character:
                    menu_active = True
                elif c == self.exit_character:
                    self.stop()
                    break
                else:
                    text = c
                    for transformation in self.tx_transformations:
                        text = transformation.tx(text)

                    self.serial.write(self.tx_encoder.encode(text))
                    if self.echo:
                        echo_text = c
                        for transformation in self.tx_transformations:
                            echo_text = transformation.echo(echo_text)

                        self.console.write(echo_text)

        except:
            self.alive = False
            raise

    def handle_menu_key(self, c):
        """Implement a simple menu / settings"""
        if c == self.menu_character or c == self.exit_character:
            self.serial.write(self.tx_encoder.encode(c))
            if self.echo:
                self.console.write(c)
        elif c == '\x15':
            sys.stderr.write('\n--- File to upload: ')
            sys.stderr.flush()
            with self.console:
                filename = sys.stdin.readline().rstrip('\r\n')
                if filename:
                    try:
                        with open(filename, 'rb') as (f):
                            sys.stderr.write(('--- Sending file {} ---\n').format(filename))
                            while True:
                                block = f.read(1024)
                                if not block:
                                    break
                                self.serial.write(block)
                                self.serial.flush()
                                sys.stderr.write('.')

                        sys.stderr.write(('\n--- File {} sent ---\n').format(filename))
                    except IOError as e:
                        sys.stderr.write(('--- ERROR opening file {}: {} ---\n').format(filename, e))

        elif c in '\x08hH?':
            sys.stderr.write(self.get_help_text())
        elif c == '\x12':
            self.serial.rts = not self.serial.rts
            sys.stderr.write(('--- RTS {} ---\n').format('active' if self.serial.rts else 'inactive'))
        elif c == '\x04':
            self.serial.dtr = not self.serial.dtr
            sys.stderr.write(('--- DTR {} ---\n').format('active' if self.serial.dtr else 'inactive'))
        elif c == '\x02':
            self.serial.break_condition = not self.serial.break_condition
            sys.stderr.write(('--- BREAK {} ---\n').format('active' if self.serial.break_condition else 'inactive'))
        elif c == '\x05':
            self.echo = not self.echo
            sys.stderr.write(('--- local echo {} ---\n').format('active' if self.echo else 'inactive'))
        elif c == '\x06':
            sys.stderr.write('\n--- Available Filters:\n')
            sys.stderr.write(('\n').join(('---   {:<10} = {.__doc__}').format(k, v) for k, v in sorted(TRANSFORMATIONS.items())))
            sys.stderr.write(('\n--- Enter new filter name(s) [{}]: ').format((' ').join(self.filters)))
            with self.console:
                new_filters = sys.stdin.readline().lower().split()
            if new_filters:
                for f in new_filters:
                    if f not in TRANSFORMATIONS:
                        sys.stderr.write(('--- unknown filter: {}').format(repr(f)))
                        break
                else:
                    self.filters = new_filters
                    self.update_transformations()

            sys.stderr.write(('--- filters: {}\n').format((' ').join(self.filters)))
        elif c == '\x0c':
            modes = list(EOL_TRANSFORMATIONS)
            eol = modes.index(self.eol) + 1
            if eol >= len(modes):
                eol = 0
            self.eol = modes[eol]
            sys.stderr.write(('--- EOL: {} ---\n').format(self.eol.upper()))
            self.update_transformations()
        elif c == '\x01':
            sys.stderr.write(('\n--- Enter new encoding name [{}]: ').format(self.input_encoding))
            with self.console:
                new_encoding = sys.stdin.readline().strip()
            if new_encoding:
                try:
                    codecs.lookup(new_encoding)
                except LookupError:
                    sys.stderr.write(('--- invalid encoding name: {}\n').format(new_encoding))
                else:
                    self.set_rx_encoding(new_encoding)
                    self.set_tx_encoding(new_encoding)

            sys.stderr.write(('--- serial input encoding: {}\n').format(self.input_encoding))
            sys.stderr.write(('--- serial output encoding: {}\n').format(self.output_encoding))
        elif c == '\t':
            self.dump_port_settings()
        elif c in 'pP':
            with self.console:
                try:
                    port = ask_for_port()
                except KeyboardInterrupt:
                    port = None

            if port and port != self.serial.port:
                self._stop_reader()
                settings = self.serial.getSettingsDict()
                try:
                    new_serial = serial.serial_for_url(port, do_not_open=True)
                    new_serial.applySettingsDict(settings)
                    new_serial.rts = self.serial.rts
                    new_serial.dtr = self.serial.dtr
                    new_serial.open()
                    new_serial.break_condition = self.serial.break_condition
                except Exception as e:
                    sys.stderr.write(('--- ERROR opening new port: {} ---\n').format(e))
                    new_serial.close()
                else:
                    self.serial.close()
                    self.serial = new_serial
                    sys.stderr.write(('--- Port changed to: {} ---\n').format(self.serial.port))

                self._start_reader()
        elif c in 'bB':
            sys.stderr.write('\n--- Baudrate: ')
            sys.stderr.flush()
            with self.console:
                backup = self.serial.baudrate
                try:
                    self.serial.baudrate = int(sys.stdin.readline().strip())
                except ValueError as e:
                    sys.stderr.write(('--- ERROR setting baudrate: %s ---\n').format(e))
                    self.serial.baudrate = backup
                else:
                    self.dump_port_settings()

        elif c == '8':
            self.serial.bytesize = serial.EIGHTBITS
            self.dump_port_settings()
        elif c == '7':
            self.serial.bytesize = serial.SEVENBITS
            self.dump_port_settings()
        elif c in 'eE':
            self.serial.parity = serial.PARITY_EVEN
            self.dump_port_settings()
        elif c in 'oO':
            self.serial.parity = serial.PARITY_ODD
            self.dump_port_settings()
        elif c in 'mM':
            self.serial.parity = serial.PARITY_MARK
            self.dump_port_settings()
        elif c in 'sS':
            self.serial.parity = serial.PARITY_SPACE
            self.dump_port_settings()
        elif c in 'nN':
            self.serial.parity = serial.PARITY_NONE
            self.dump_port_settings()
        elif c == '1':
            self.serial.stopbits = serial.STOPBITS_ONE
            self.dump_port_settings()
        elif c == '2':
            self.serial.stopbits = serial.STOPBITS_TWO
            self.dump_port_settings()
        elif c == '3':
            self.serial.stopbits = serial.STOPBITS_ONE_POINT_FIVE
            self.dump_port_settings()
        elif c in 'xX':
            self.serial.xonxoff = c == 'X'
            self.dump_port_settings()
        elif c in 'rR':
            self.serial.rtscts = c == 'R'
            self.dump_port_settings()
        else:
            sys.stderr.write(('--- unknown menu character {} --\n').format(key_description(c)))
        return

    def get_help_text(self):
        return ('\n--- pySerial ({version}) - miniterm - help\n---\n--- {exit:8} Exit program\n--- {menu:8} Menu escape key, followed by:\n--- Menu keys:\n---    {menu:7} Send the menu character itself to remote\n---    {exit:7} Send the exit character itself to remote\n---    {info:7} Show info\n---    {upload:7} Upload file (prompt will be shown)\n---    {repr:7} encoding\n---    {filter:7} edit filters\n--- Toggles:\n---    {rts:7} RTS   {dtr:7} DTR   {brk:7} BREAK\n---    {echo:7} echo  {eol:7} EOL\n---\n--- Port settings ({menu} followed by the following):\n---    p          change port\n---    7 8        set data bits\n---    N E O S M  change parity (None, Even, Odd, Space, Mark)\n---    1 2 3      set stop bits (1, 2, 1.5)\n---    b          change baud rate\n---    x X        disable/enable software flow control\n---    r R        disable/enable hardware flow control\n').format(version=getattr(serial, 'VERSION', 'unknown version'), exit=key_description(self.exit_character), menu=key_description(self.menu_character), rts=key_description('\x12'), dtr=key_description('\x04'), brk=key_description('\x02'), echo=key_description('\x05'), info=key_description('\t'), upload=key_description('\x15'), repr=key_description('\x01'), filter=key_description('\x06'), eol=key_description('\x0c'))


def main(default_port=None, default_baudrate=9600, default_rts=None, default_dtr=None):
    import argparse
    parser = argparse.ArgumentParser(description='Miniterm - A simple terminal program for the serial port.')
    parser.add_argument('port', nargs='?', help="serial port name ('-' to show port list)", default=default_port)
    parser.add_argument('baudrate', nargs='?', type=int, help='set baud rate, default: %(default)s', default=default_baudrate)
    group = parser.add_argument_group('port settings')
    group.add_argument('--parity', choices=[
     'N', 'E', 'O', 'S', 'M'], type=lambda c: c.upper(), help='set parity, one of {N E O S M}, default: N', default='N')
    group.add_argument('--rtscts', action='store_true', help='enable RTS/CTS flow control (default off)', default=False)
    group.add_argument('--xonxoff', action='store_true', help='enable software flow control (default off)', default=False)
    group.add_argument('--rts', type=int, help='set initial RTS line state (possible values: 0, 1)', default=default_rts)
    group.add_argument('--dtr', type=int, help='set initial DTR line state (possible values: 0, 1)', default=default_dtr)
    group = parser.add_argument_group('data handling')
    group.add_argument('-e', '--echo', action='store_true', help='enable local echo (default off)', default=False)
    group.add_argument('--encoding', dest='serial_port_encoding', metavar='CODEC', help='set the encoding for the serial port (e.g. hexlify, Latin1, UTF-8), default: %(default)s', default='UTF-8')
    group.add_argument('-f', '--filter', action='append', metavar='NAME', help='add text transformation', default=[])
    group.add_argument('--eol', choices=[
     'CR', 'LF', 'CRLF'], type=lambda c: c.upper(), help='end of line mode', default='CRLF')
    group.add_argument('--raw', action='store_true', help='Do no apply any encodings/transformations', default=False)
    group = parser.add_argument_group('hotkeys')
    group.add_argument('--exit-char', type=int, metavar='NUM', help='Unicode of special character that is used to exit the application, default: %(default)s', default=29)
    group.add_argument('--menu-char', type=int, metavar='NUM', help='Unicode code of special character that is used to control miniterm (menu), default: %(default)s', default=20)
    group = parser.add_argument_group('diagnostics')
    group.add_argument('-q', '--quiet', action='store_true', help='suppress non-error messages', default=False)
    group.add_argument('--develop', action='store_true', help='show Python traceback on error', default=False)
    args = parser.parse_args()
    if args.menu_char == args.exit_char:
        parser.error('--exit-char can not be the same as --menu-char')
    if args.port is None or args.port == '-':
        try:
            args.port = ask_for_port()
        except KeyboardInterrupt:
            sys.stderr.write('\n')
            parser.error('user aborted and port is not given')
        else:
            if not args.port:
                parser.error('port is not given')
    if args.filter:
        if 'help' in args.filter:
            sys.stderr.write('Available filters:\n')
            sys.stderr.write(('\n').join(('{:<10} = {.__doc__}').format(k, v) for k, v in sorted(TRANSFORMATIONS.items())))
            sys.stderr.write('\n')
            sys.exit(1)
        filters = args.filter
    else:
        filters = [
         'default']
    try:
        serial_instance = serial.serial_for_url(args.port, args.baudrate, parity=args.parity, rtscts=args.rtscts, xonxoff=args.xonxoff, timeout=1, do_not_open=True)
        if args.dtr is not None:
            if not args.quiet:
                sys.stderr.write(('--- forcing DTR {}\n').format('active' if args.dtr else 'inactive'))
            serial_instance.dtr = args.dtr
        if args.rts is not None:
            if not args.quiet:
                sys.stderr.write(('--- forcing RTS {}\n').format('active' if args.rts else 'inactive'))
            serial_instance.rts = args.rts
        serial_instance.open()
    except serial.SerialException as e:
        sys.stderr.write(('could not open port {}: {}\n').format(repr(args.port), e))
        if args.develop:
            raise
        sys.exit(1)

    miniterm = Miniterm(serial_instance, echo=args.echo, eol=args.eol.lower(), filters=filters)
    miniterm.exit_character = unichr(args.exit_char)
    miniterm.menu_character = unichr(args.menu_char)
    miniterm.raw = args.raw
    miniterm.set_rx_encoding(args.serial_port_encoding)
    miniterm.set_tx_encoding(args.serial_port_encoding)
    if not args.quiet:
        sys.stderr.write(('--- Miniterm on {p.name}  {p.baudrate},{p.bytesize},{p.parity},{p.stopbits} ---\n').format(p=miniterm.serial))
        sys.stderr.write(('--- Quit: {} | Menu: {} | Help: {} followed by {} ---\n').format(key_description(miniterm.exit_character), key_description(miniterm.menu_character), key_description(miniterm.menu_character), key_description('\x08')))
    miniterm.start()
    try:
        miniterm.join(True)
    except KeyboardInterrupt:
        pass

    if not args.quiet:
        sys.stderr.write('\n--- exit ---\n')
    miniterm.join()
    return


if __name__ == '__main__':
    main()