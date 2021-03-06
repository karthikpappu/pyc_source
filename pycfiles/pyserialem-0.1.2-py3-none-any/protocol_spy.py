# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/urlhandler/protocol_spy.py
# Compiled at: 2015-08-29 23:00:32
import sys, time, serial
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

def sixteen(data):
    """    yield tuples of hex and ASCII display in multiples of 16. Includes a
    space after 8 bytes and (None, None) after 16 bytes and at the end.
    """
    n = 0
    for b in serial.iterbytes(data):
        yield (
         ('{:02X} ').format(ord(b)), b.decode('ascii') if ' ' <= b < '\x7f' else '.')
        n += 1
        if n == 8:
            yield (' ', '')
        elif n >= 16:
            yield (None, None)
            n = 0

    if n > 0:
        while n < 16:
            n += 1
            if n == 8:
                yield (' ', '')
            yield ('   ', ' ')

        yield (None, None)
    return


def hexdump(data):
    """yield lines with hexdump of data"""
    values = []
    ascii = []
    offset = 0
    for h, a in sixteen(data):
        if h is None:
            yield (
             offset,
             (' ').join([
              ('').join(values),
              ('').join(ascii)]))
            del values[:]
            del ascii[:]
            offset += 16
        else:
            values.append(h)
            ascii.append(a)

    return


class FormatRaw(object):
    """Forward only RX and TX data to output."""

    def __init__(self, output, color):
        self.output = output
        self.color = color
        self.rx_color = '\x1b[32m'
        self.tx_color = '\x1b[31m'

    def rx(self, data):
        if self.color:
            self.output.write(self.rx_color)
        self.output.write(data)
        self.output.flush()

    def tx(self, data):
        if self.color:
            self.output.write(self.tx_color)
        self.output.write(data)
        self.output.flush()

    def control(self, name, value):
        pass


class FormatHexdump(object):
    """    Create a hex dump of RX ad TX data, show when control lines are read or
    written.

    output example::

        000000.000 Q-RX flushInput
        000002.469 RTS  inactive
        000002.773 RTS  active
        000003.001 TX   48 45 4C 4C 4F                                    HELLO
        000003.102 RX   48 45 4C 4C 4F                                    HELLO

    """

    def __init__(self, output, color):
        self.start_time = time.time()
        self.output = output
        self.color = color
        self.rx_color = '\x1b[32m'
        self.tx_color = '\x1b[31m'
        self.control_color = '\x1b[37m'

    def write_line(self, timestamp, label, value, value2=''):
        self.output.write(('{:010.3f} {:4} {}{}\n').format(timestamp, label, value, value2))
        self.output.flush()

    def rx(self, data):
        if self.color:
            self.output.write(self.rx_color)
        if data:
            for offset, row in hexdump(data):
                self.write_line(time.time() - self.start_time, 'RX', ('{:04X}  ').format(offset), row)

        else:
            self.write_line(time.time() - self.start_time, 'RX', '<empty>')

    def tx(self, data):
        if self.color:
            self.output.write(self.tx_color)
        for offset, row in hexdump(data):
            self.write_line(time.time() - self.start_time, 'TX', ('{:04X}  ').format(offset), row)

    def control(self, name, value):
        if self.color:
            self.output.write(self.control_color)
        self.write_line(time.time() - self.start_time, name, value)


class Serial(serial.Serial):
    """Just inherit the native Serial port implementation and patch the port property."""

    def __init__(self, *args, **kwargs):
        super(Serial, self).__init__(*args, **kwargs)
        self.formatter = None
        self.show_all = False
        return

    @serial.Serial.port.setter
    def port(self, value):
        if value is not None:
            serial.Serial.port.__set__(self, self.from_url(value))
        return

    def from_url(self, url):
        """extract host and port from an URL string"""
        parts = urlparse.urlsplit(url)
        if parts.scheme != 'spy':
            raise serial.SerialException('expected a string in the form "spy://port[?option[=value][&option[=value]]]": not starting with spy:// (%r)' % (parts.scheme,))
        formatter = FormatHexdump
        color = False
        output = sys.stderr
        try:
            for option, values in urlparse.parse_qs(parts.query, True).items():
                if option == 'file':
                    output = open(values[0], 'w')
                elif option == 'color':
                    color = True
                elif option == 'raw':
                    formatter = FormatRaw
                elif option == 'all':
                    self.show_all = True
                else:
                    raise ValueError('unknown option: %r' % (option,))

        except ValueError as e:
            raise serial.SerialException('expected a string in the form "spy://port[?option[=value][&option[=value]]]": %s' % e)

        self.formatter = formatter(output, color)
        return ('').join([parts.netloc, parts.path])

    def write(self, tx):
        self.formatter.tx(tx)
        return super(Serial, self).write(tx)

    def read(self, size=1):
        rx = super(Serial, self).read(size)
        if rx or self.show_all:
            self.formatter.rx(rx)
        return rx

    @property
    def in_waiting(self):
        n = super(Serial, self).in_waiting
        if self.show_all:
            self.formatter.control('Q-RX', ('in_waiting -> {}').format(n))
        return n

    def flush(self):
        self.formatter.control('Q-TX', 'flush')
        super(Serial, self).flush()

    def reset_input_buffer(self):
        self.formatter.control('Q-RX', 'reset_input_buffer')
        super(Serial, self).reset_input_buffer()

    def reset_output_buffer(self):
        self.formatter.control('Q-TX', 'reset_output_buffer')
        super(Serial, self).reset_output_buffer()

    def send_break(self, duration=0.25):
        self.formatter.control('BRK', ('send_break {}s').format(duration))
        super(Serial, self).send_break(duration)

    @serial.Serial.break_condition.setter
    def break_condition(self, level):
        self.formatter.control('BRK', 'active' if level else 'inactive')
        serial.Serial.break_condition.__set__(self, level)

    @serial.Serial.rts.setter
    def rts(self, level):
        self.formatter.control('RTS', 'active' if level else 'inactive')
        serial.Serial.rts.__set__(self, level)

    @serial.Serial.dtr.setter
    def dtr(self, level):
        self.formatter.control('DTR', 'active' if level else 'inactive')
        serial.Serial.dtr.__set__(self, level)

    @serial.Serial.cts.getter
    def cts(self):
        level = super(Serial, self).cts
        self.formatter.control('CTS', 'active' if level else 'inactive')
        return level

    @serial.Serial.dsr.getter
    def dsr(self):
        level = super(Serial, self).dsr
        self.formatter.control('DSR', 'active' if level else 'inactive')
        return level

    @serial.Serial.ri.getter
    def ri(self):
        level = super(Serial, self).ri
        self.formatter.control('RI', 'active' if level else 'inactive')
        return level

    @serial.Serial.cd.getter
    def cd(self):
        level = super(Serial, self).cd
        self.formatter.control('CD', 'active' if level else 'inactive')
        return level


if __name__ == '__main__':
    s = Serial(None)
    s.port = 'spy:///dev/ttyS0'
    print s