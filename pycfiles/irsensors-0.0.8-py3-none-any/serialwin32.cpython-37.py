# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ISEN\AppData\Local\Temp\pip-install-57ghrzot\pyserial\serial\serialwin32.py
# Compiled at: 2019-09-23 21:15:07
# Size of source mod 2**32: 20087 bytes
import ctypes, time
from serial import win32
import serial
from serial.serialutil import SerialBase, SerialException, to_bytes, portNotOpenError, writeTimeoutError

class Serial(SerialBase):
    __doc__ = 'Serial port implementation for Win32 based on ctypes.'
    BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600,
                 19200, 38400, 57600, 115200)

    def __init__(self, *args, **kwargs):
        self._port_handle = None
        self._overlapped_read = None
        self._overlapped_write = None
        (super(Serial, self).__init__)(*args, **kwargs)

    def open(self):
        """        Open port with current settings. This may throw a SerialException
        if the port cannot be opened.
        """
        if self._port is None:
            raise SerialException('Port must be configured before it can be used.')
        else:
            if self.is_open:
                raise SerialException('Port is already open.')
            port = self.name
            try:
                if port.upper().startswith('COM'):
                    if int(port[3:]) > 8:
                        port = '\\\\.\\' + port
            except ValueError:
                pass

        self._port_handle = win32.CreateFile(port, win32.GENERIC_READ | win32.GENERIC_WRITE, 0, None, win32.OPEN_EXISTING, win32.FILE_ATTRIBUTE_NORMAL | win32.FILE_FLAG_OVERLAPPED, 0)
        if self._port_handle == win32.INVALID_HANDLE_VALUE:
            self._port_handle = None
            raise SerialException('could not open port {!r}: {!r}'.format(self.portstr, ctypes.WinError()))
        try:
            self._overlapped_read = win32.OVERLAPPED()
            self._overlapped_read.hEvent = win32.CreateEvent(None, 1, 0, None)
            self._overlapped_write = win32.OVERLAPPED()
            self._overlapped_write.hEvent = win32.CreateEvent(None, 0, 0, None)
            win32.SetupComm(self._port_handle, 4096, 4096)
            self._orgTimeouts = win32.COMMTIMEOUTS()
            win32.GetCommTimeouts(self._port_handle, ctypes.byref(self._orgTimeouts))
            self._reconfigure_port()
            win32.PurgeComm(self._port_handle, win32.PURGE_TXCLEAR | win32.PURGE_TXABORT | win32.PURGE_RXCLEAR | win32.PURGE_RXABORT)
        except:
            try:
                self._close()
            except:
                pass

            self._port_handle = None
            raise
        else:
            self.is_open = True

    def _reconfigure_port(self):
        """Set communication parameters on opened port."""
        if not self._port_handle:
            raise SerialException('Can only operate on a valid port handle')
        else:
            timeouts = win32.COMMTIMEOUTS()
            if self._timeout is None:
                pass
            elif self._timeout == 0:
                timeouts.ReadIntervalTimeout = win32.MAXDWORD
            else:
                timeouts.ReadTotalTimeoutConstant = max(int(self._timeout * 1000), 1)
            if self._timeout != 0:
                if self._inter_byte_timeout is not None:
                    timeouts.ReadIntervalTimeout = max(int(self._inter_byte_timeout * 1000), 1)
            else:
                if self._write_timeout is None:
                    pass
                elif self._write_timeout == 0:
                    timeouts.WriteTotalTimeoutConstant = win32.MAXDWORD
                else:
                    timeouts.WriteTotalTimeoutConstant = max(int(self._write_timeout * 1000), 1)
                win32.SetCommTimeouts(self._port_handle, ctypes.byref(timeouts))
                win32.SetCommMask(self._port_handle, win32.EV_ERR)
                comDCB = win32.DCB()
                win32.GetCommState(self._port_handle, ctypes.byref(comDCB))
                comDCB.BaudRate = self._baudrate
                if self._bytesize == serial.FIVEBITS:
                    comDCB.ByteSize = 5
                else:
                    if self._bytesize == serial.SIXBITS:
                        comDCB.ByteSize = 6
                    else:
                        if self._bytesize == serial.SEVENBITS:
                            comDCB.ByteSize = 7
                        else:
                            if self._bytesize == serial.EIGHTBITS:
                                comDCB.ByteSize = 8
                            else:
                                raise ValueError('Unsupported number of data bits: {!r}'.format(self._bytesize))
                if self._parity == serial.PARITY_NONE:
                    comDCB.Parity = win32.NOPARITY
                    comDCB.fParity = 0
                else:
                    if self._parity == serial.PARITY_EVEN:
                        comDCB.Parity = win32.EVENPARITY
                        comDCB.fParity = 1
                    else:
                        if self._parity == serial.PARITY_ODD:
                            comDCB.Parity = win32.ODDPARITY
                            comDCB.fParity = 1
                        else:
                            if self._parity == serial.PARITY_MARK:
                                comDCB.Parity = win32.MARKPARITY
                                comDCB.fParity = 1
                            else:
                                if self._parity == serial.PARITY_SPACE:
                                    comDCB.Parity = win32.SPACEPARITY
                                    comDCB.fParity = 1
                                else:
                                    raise ValueError('Unsupported parity mode: {!r}'.format(self._parity))
                if self._stopbits == serial.STOPBITS_ONE:
                    comDCB.StopBits = win32.ONESTOPBIT
                else:
                    if self._stopbits == serial.STOPBITS_ONE_POINT_FIVE:
                        comDCB.StopBits = win32.ONE5STOPBITS
                    else:
                        if self._stopbits == serial.STOPBITS_TWO:
                            comDCB.StopBits = win32.TWOSTOPBITS
                        else:
                            raise ValueError('Unsupported number of stop bits: {!r}'.format(self._stopbits))
                comDCB.fBinary = 1
                if self._rs485_mode is None:
                    if self._rtscts:
                        comDCB.fRtsControl = win32.RTS_CONTROL_HANDSHAKE
                    else:
                        comDCB.fRtsControl = win32.RTS_CONTROL_ENABLE if self._rts_state else win32.RTS_CONTROL_DISABLE
                    comDCB.fOutxCtsFlow = self._rtscts
                else:
                    if not self._rs485_mode.rts_level_for_tx:
                        raise ValueError('Unsupported value for RS485Settings.rts_level_for_tx: {!r}'.format(self._rs485_mode.rts_level_for_tx))
                    if self._rs485_mode.rts_level_for_rx:
                        raise ValueError('Unsupported value for RS485Settings.rts_level_for_rx: {!r}'.format(self._rs485_mode.rts_level_for_rx))
                    if self._rs485_mode.delay_before_tx is not None:
                        raise ValueError('Unsupported value for RS485Settings.delay_before_tx: {!r}'.format(self._rs485_mode.delay_before_tx))
                    if self._rs485_mode.delay_before_rx is not None:
                        raise ValueError('Unsupported value for RS485Settings.delay_before_rx: {!r}'.format(self._rs485_mode.delay_before_rx))
                    if self._rs485_mode.loopback:
                        raise ValueError('Unsupported value for RS485Settings.loopback: {!r}'.format(self._rs485_mode.loopback))
                    comDCB.fRtsControl = win32.RTS_CONTROL_TOGGLE
                    comDCB.fOutxCtsFlow = 0
                if self._dsrdtr:
                    comDCB.fDtrControl = win32.DTR_CONTROL_HANDSHAKE
                else:
                    comDCB.fDtrControl = win32.DTR_CONTROL_ENABLE if self._dtr_state else win32.DTR_CONTROL_DISABLE
            comDCB.fOutxDsrFlow = self._dsrdtr
            comDCB.fOutX = self._xonxoff
            comDCB.fInX = self._xonxoff
            comDCB.fNull = 0
            comDCB.fErrorChar = 0
            comDCB.fAbortOnError = 0
            comDCB.XonChar = serial.XON
            comDCB.XoffChar = serial.XOFF
            assert win32.SetCommState(self._port_handle, ctypes.byref(comDCB)), 'Cannot configure port, something went wrong. Original message: {!r}'.format(ctypes.WinError())

    def _close(self):
        """internal close port helper"""
        if self._port_handle is not None:
            win32.SetCommTimeouts(self._port_handle, self._orgTimeouts)
            if self._overlapped_read is not None:
                self.cancel_read()
                win32.CloseHandle(self._overlapped_read.hEvent)
                self._overlapped_read = None
            if self._overlapped_write is not None:
                self.cancel_write()
                win32.CloseHandle(self._overlapped_write.hEvent)
                self._overlapped_write = None
            win32.CloseHandle(self._port_handle)
            self._port_handle = None

    def close(self):
        """Close port"""
        if self.is_open:
            self._close()
            self.is_open = False

    @property
    def in_waiting(self):
        """Return the number of bytes currently in the input buffer."""
        flags = win32.DWORD()
        comstat = win32.COMSTAT()
        if not win32.ClearCommError(self._port_handle, ctypes.byref(flags), ctypes.byref(comstat)):
            raise SerialException('ClearCommError failed ({!r})'.format(ctypes.WinError()))
        return comstat.cbInQue

    def read(self, size=1):
        """        Read size bytes from the serial port. If a timeout is set it may
        return less characters as requested. With no timeout it will block
        until the requested number of bytes is read.
        """
        if not self.is_open:
            raise portNotOpenError
        elif size > 0:
            win32.ResetEvent(self._overlapped_read.hEvent)
            flags = win32.DWORD()
            comstat = win32.COMSTAT()
            if not win32.ClearCommError(self._port_handle, ctypes.byref(flags), ctypes.byref(comstat)):
                raise SerialException('ClearCommError failed ({!r})'.format(ctypes.WinError()))
            else:
                n = min(comstat.cbInQue, size) if self.timeout == 0 else size
                if n > 0:
                    buf = ctypes.create_string_buffer(n)
                    rc = win32.DWORD()
                    read_ok = win32.ReadFile(self._port_handle, buf, n, ctypes.byref(rc), ctypes.byref(self._overlapped_read))
                    if not read_ok:
                        if win32.GetLastError() not in (win32.ERROR_SUCCESS, win32.ERROR_IO_PENDING):
                            raise SerialException('ReadFile failed ({!r})'.format(ctypes.WinError()))
                    result_ok = win32.GetOverlappedResult(self._port_handle, ctypes.byref(self._overlapped_read), ctypes.byref(rc), True)
                    if not result_ok:
                        if win32.GetLastError() != win32.ERROR_OPERATION_ABORTED:
                            raise SerialException('GetOverlappedResult failed ({!r})'.format(ctypes.WinError()))
                        read = buf.raw[:rc.value]
                    else:
                        pass
                read = bytes()
        else:
            read = bytes()
        return bytes(read)

    def write(self, data):
        """Output the given byte string over the serial port."""
        if not self.is_open:
            raise portNotOpenError
        else:
            data = to_bytes(data)
            if data:
                n = win32.DWORD()
                success = win32.WriteFile(self._port_handle, data, len(data), ctypes.byref(n), self._overlapped_write)
                if self._write_timeout != 0:
                    if not success:
                        if win32.GetLastError() not in (win32.ERROR_SUCCESS, win32.ERROR_IO_PENDING):
                            raise SerialException('WriteFile failed ({!r})'.format(ctypes.WinError()))
                    win32.GetOverlappedResult(self._port_handle, self._overlapped_write, ctypes.byref(n), True)
                    if win32.GetLastError() == win32.ERROR_OPERATION_ABORTED:
                        return n.value
                    if n.value != len(data):
                        raise writeTimeoutError
                    return n.value
                errorcode = win32.ERROR_SUCCESS if success else win32.GetLastError()
                if errorcode in (win32.ERROR_INVALID_USER_BUFFER, win32.ERROR_NOT_ENOUGH_MEMORY,
                 win32.ERROR_OPERATION_ABORTED):
                    return 0
                if errorcode in (win32.ERROR_SUCCESS, win32.ERROR_IO_PENDING):
                    return len(data)
                raise SerialException('WriteFile failed ({!r})'.format(ctypes.WinError()))
            else:
                return 0

    def flush(self):
        """        Flush of file like objects. In this case, wait until all data
        is written.
        """
        while self.out_waiting:
            time.sleep(0.05)

    def reset_input_buffer(self):
        """Clear input buffer, discarding all that is in the buffer."""
        if not self.is_open:
            raise portNotOpenError
        win32.PurgeComm(self._port_handle, win32.PURGE_RXCLEAR | win32.PURGE_RXABORT)

    def reset_output_buffer(self):
        """        Clear output buffer, aborting the current output and discarding all
        that is in the buffer.
        """
        if not self.is_open:
            raise portNotOpenError
        win32.PurgeComm(self._port_handle, win32.PURGE_TXCLEAR | win32.PURGE_TXABORT)

    def _update_break_state(self):
        """Set break: Controls TXD. When active, to transmitting is possible."""
        if not self.is_open:
            raise portNotOpenError
        elif self._break_state:
            win32.SetCommBreak(self._port_handle)
        else:
            win32.ClearCommBreak(self._port_handle)

    def _update_rts_state(self):
        """Set terminal status line: Request To Send"""
        if self._rts_state:
            win32.EscapeCommFunction(self._port_handle, win32.SETRTS)
        else:
            win32.EscapeCommFunction(self._port_handle, win32.CLRRTS)

    def _update_dtr_state(self):
        """Set terminal status line: Data Terminal Ready"""
        if self._dtr_state:
            win32.EscapeCommFunction(self._port_handle, win32.SETDTR)
        else:
            win32.EscapeCommFunction(self._port_handle, win32.CLRDTR)

    def _GetCommModemStatus(self):
        if not self.is_open:
            raise portNotOpenError
        stat = win32.DWORD()
        win32.GetCommModemStatus(self._port_handle, ctypes.byref(stat))
        return stat.value

    @property
    def cts(self):
        """Read terminal status line: Clear To Send"""
        return win32.MS_CTS_ON & self._GetCommModemStatus() != 0

    @property
    def dsr(self):
        """Read terminal status line: Data Set Ready"""
        return win32.MS_DSR_ON & self._GetCommModemStatus() != 0

    @property
    def ri(self):
        """Read terminal status line: Ring Indicator"""
        return win32.MS_RING_ON & self._GetCommModemStatus() != 0

    @property
    def cd(self):
        """Read terminal status line: Carrier Detect"""
        return win32.MS_RLSD_ON & self._GetCommModemStatus() != 0

    def set_buffer_size(self, rx_size=4096, tx_size=None):
        """        Recommend a buffer size to the driver (device driver can ignore this
        value). Must be called before the port is opened.
        """
        if tx_size is None:
            tx_size = rx_size
        win32.SetupComm(self._port_handle, rx_size, tx_size)

    def set_output_flow_control(self, enable=True):
        """        Manually control flow - when software flow control is enabled.
        This will do the same as if XON (true) or XOFF (false) are received
        from the other device and control the transmission accordingly.
        WARNING: this function is not portable to different platforms!
        """
        if not self.is_open:
            raise portNotOpenError
        elif enable:
            win32.EscapeCommFunction(self._port_handle, win32.SETXON)
        else:
            win32.EscapeCommFunction(self._port_handle, win32.SETXOFF)

    @property
    def out_waiting(self):
        """Return how many bytes the in the outgoing buffer"""
        flags = win32.DWORD()
        comstat = win32.COMSTAT()
        if not win32.ClearCommError(self._port_handle, ctypes.byref(flags), ctypes.byref(comstat)):
            raise SerialException('ClearCommError failed ({!r})'.format(ctypes.WinError()))
        return comstat.cbOutQue

    def _cancel_overlapped_io(self, overlapped):
        """Cancel a blocking read operation, may be called from other thread"""
        rc = win32.DWORD()
        err = win32.GetOverlappedResult(self._port_handle, ctypes.byref(overlapped), ctypes.byref(rc), False)
        if not err:
            if win32.GetLastError() in (win32.ERROR_IO_PENDING, win32.ERROR_IO_INCOMPLETE):
                win32.CancelIoEx(self._port_handle, overlapped)

    def cancel_read(self):
        """Cancel a blocking read operation, may be called from other thread"""
        self._cancel_overlapped_io(self._overlapped_read)

    def cancel_write(self):
        """Cancel a blocking write operation, may be called from other thread"""
        self._cancel_overlapped_io(self._overlapped_write)

    @SerialBase.exclusive.setter
    def exclusive(self, exclusive):
        """Change the exclusive access setting."""
        if exclusive is not None and not exclusive:
            raise ValueError('win32 only supports exclusive access (not: {})'.format(exclusive))
        else:
            serial.SerialBase.exclusive.__set__(self, exclusive)