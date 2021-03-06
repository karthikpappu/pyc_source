# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/python/win32.py
# Compiled at: 2020-04-11 22:12:39
# Size of source mod 2**32: 8689 bytes
from __future__ import print_function, division, absolute_import
import sys
if 'win' in sys.platform:
    import ctypes, ctypes.wintypes
GWL_WNDPROC = -4
GWL_HINSTANCE = -6
GWL_HWNDPARENT = -8
GWL_STYLE = -16
GWL_EXSTYLE = -20
GWL_USERDATA = -21
GWL_ID = -12
WS_BORDER = 8388608
WS_CAPTION = 12582912
WS_CHILD = 1073741824
WS_CHILDWINDOW = 1073741824
WS_CLIPCHILDREN = 33554432
WS_CLIPSIBLINGS = 67108864
WS_DISABLED = 134217728
WS_DLGFRAME = 4194304
WS_GROUP = 131072
WS_HSCROLL = 1048576
WS_ICONIC = 536870912
WS_MAXIMIZE = 16777216
WS_MAXIMIZEBOX = 65536
WS_MINIMIZE = 536870912
WS_MINIMIZEBOX = 131072
WS_OVERLAPPED = 0
WS_OVERLAPPEDWINDOW = 13565952
WS_POPUP = 2147483648
WS_POPUPWINDOW = 2156396544
WS_SIZEBOX = 262144
WS_SYSMENU = 524288
WS_TABSTOP = 65536
WS_THICKFRAME = 262144
WS_TILED = 0
WS_TILEDWINDOW = 13565952
WS_VISIBLE = 268435456
WS_VSCROLL = 2097152

def to_hwnd(pycobject):
    """
    Convenience method to get a Windows Handle from a PySide WinID
    Based on http://srinikom.github.io/pyside-bz-archive/523.html
    @return A value equivalent to a void* that represents the Windows handle if one exists; None otherwise.
    """
    if type(pycobject) is long:
        return pycobject
    else:
        if sys.version_info[0] == 2:
            ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
            ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
            return ctypes.pythonapi.PyCObject_AsVoidPtr(pycobject)
        if sys.version_info[0] == 3:
            ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
            ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object]
            return ctypes.pythonapi.PyCapsule_GetPointer(pycobject, None)


def set_owner(hwnd, hwnd_owner):
    """
    Changes the owner window of the given window
    :param hwnd:
    :param hwnd_owner:
    """
    _update_window = ctypes.windll.user32.UpdateWindow
    if ctypes.sizeof(ctypes.wintypes.HWND) == ctypes.sizeof(ctypes.c_long):
        _LONG = ctypes.wintypes.LONG
        _set_window_long = ctypes.windll.user32.SetWindowLongW
        _set_window_long.argtypes = [ctypes.wintypes.HWND, ctypes.c_int, ctypes.wintypes.LONG]
        _set_window_long.restype = ctypes.c_void_p
    else:
        if ctypes.sizeof(ctypes.wintypes.HWND) == ctypes.sizeof(ctypes.c_longlong):
            _LONG = ctypes.wintypes.HWND
            _set_window_long = ctypes.windll.user32.SetWindowLongPtrW
            _set_window_long.argtypes = [ctypes.wintypes.HWND, ctypes.c_int, ctypes.wintypes.HWND]
            _set_window_long.restype = _LONG
    last_error = ctypes.set_last_error(0)
    try:
        result = _set_window_long(ctypes.wintypes.HWND(hwnd), ctypes.c_int(GWL_HWNDPARENT), _LONG(hwnd_owner))
    finally:
        last_error = ctypes.set_last_error(last_error)

    if not result:
        if last_error:
            raise ctypes.WinError(last_error)
    _update_window(hwnd_owner)
    return result


def get_reg_key(registry, key, architecture=None):
    """
    Returns a _winreg hkey if found
    :param registry: str, registry to look in. HKEY_LOCAL_MACHINE for example
    :param key: str, key to open 'Software/Ubisoft/Test' for example
    :param architecture: variant, int || None, 32 or 64 bit. If None, default system architecture is used
    :return: _winreg handle object
    """
    import _winreg
    reg_key = None
    a_reg = _winreg.ConnectRegistry(None, getattr(_winreg, registry))
    if architecture == 32:
        sam = _winreg.KEY_WOW64_32KEY
    else:
        if architecture == 64:
            sam = _winreg.KEY_WOW64_64KEY
        else:
            sam = 0
    try:
        reg_key = _winreg.OpenKey(a_reg, key, 0, _winreg.KEY_READ | sam)
    except WindowsError:
        pass

    return reg_key


def list_reg_keys(registry, key, architecture=None):
    """
    Returns a list of child keys as tuples containing:
        - A string that identifies the value name
        - An object that holds the value data, and whose type depends on the underlying registry type
        - An integer that identifies the type of the value data (see table in docs for _winreg.SetValueEx)
    :param registry: str, registry to look in. HKEY_LOCAL_MACHINE for example
    :param key: str, key to open 'Software/Ubisoft/Test' for example
    :param architecture: variant, int || None, 32 or 64 bit. If None, default system architecture is used
    :return: list<tuple>
    """
    import _winreg
    reg_key = get_reg_key(registry=registry, key=key, architecture=architecture)
    ret = list()
    if reg_key:
        i = 0
        while True:
            try:
                ret.append(_winreg.EnumKey(reg_key, i))
                i += 1
            except WindowsError:
                break

    return ret


def list_reg_key_values(registry, key, architecture=None):
    """
    Returns a list of child keys and their values as tuples containing:
        - A string that identifies the value name
        - An object that holds the value data, and whose type depends on the underlying registry type
        - An integer that identifies the type of the value data (see table in docs for _winreg.SetValueEx)
    :param registry: str, registry to look in. HKEY_LOCAL_MACHINE for example
    :param key: str, key to open 'Software/Ubisoft/Test' for example
    :param architecture: variant, int || None, 32 or 64 bit. If None, default system architecture is used
    :return: list<tuple>
    """
    import _winreg
    reg_key = get_reg_key(registry=registry, key=key, architecture=architecture)
    ret = list()
    if reg_key:
        sub_keys, value_count, modified = _winreg.QueryInfoKey(reg_key)
        for i in range(value_count):
            ret.append(_winreg.EnumValue(reg_key, i))

    return ret


def registry_value(registry, key, value_name, architecture=None):
    """
    Retruns the value and type of the given registry key value name
    :param registry: str, registry to look in. HKEY_LOCAL_MACHINE for example
    :param key: str, key to open 'Software/Ubisoft/Test' for example
    :param value_name: str, name of the value to read. To read the 'default' key, pass an empty string
    :param architecture: variant, int || None, 32 or 64 bit. If None, default system architecture is used
    :return: tuple<object, int, value stored in key and registry type for value (see _winreg's Value Types)
    """
    reg_key = get_reg_key(registry, key, architecture=architecture)
    if reg_key:
        import _winreg
        value = _winreg.QueryValueEx(reg_key, value_name)
        _winreg.CloseKey(reg_key)
        return value
    else:
        return ('', 0)


def get_monitors():
    """
    Returns a list of all monitors
    code.activestate.com/recipes/460509-get-the-actual-and-usable-sizes-of-all-the-monitor
    :return:
    """
    result = list()
    CBFUNC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_double)

    def cb(h_monitor, hdc_monitor, l_prc_monitor, dw_data):
        r = l_prc_monitor.contents
        data = [h_monitor]
        data.append(r.dump())
        result.append(data)
        return 1

    cb_fn = CBFUNC(cb)
    ctypes.windll.user32.EnumDisplayMonitors(0, 0, cb_fn, 0)
    return result


def get_active_monitor_area():
    """
    Returns the active and working area of each monitor
    code.activestate.com/recipes/460509-get-the-actual-and-usable-sizes-of-all-the-monitor
    :return:
    """
    result = list()
    monitors = get_monitors()
    for h_monitor, extents in monitors:
        data = [
         h_monitor]
        monitor_info = MonitorInfo()
        monitor_info.cbSize = ctypes.sizeof(MonitorInfo)
        monitor_info.rcMonitor = Rect()
        monitor_info.rcWork = Rect()
        ctypes.windll.user32.GetMonitorInfoA(h_monitor, ctypes.byref(monitor_info))
        data.append(monitor_info.rcMonitor.dump())
        data.append(monitor_info.rcWork.dump())
        result.append(data)

    return result


class Rect(ctypes.Structure):
    _fields_ = [
     (
      'left', ctypes.c_long),
     (
      'top', ctypes.c_long),
     (
      'right', ctypes.c_long),
     (
      'bottom', ctypes.c_long)]

    def dump(self):
        return tuple(map(int, (self.left, self.top, self.right, self.bottom)))


class MonitorInfo(ctypes.Structure):
    _fields_ = [
     (
      'cbSize', ctypes.c_long),
     (
      'rcMonitor', Rect),
     (
      'rcWork', Rect),
     (
      'dwFlags', ctypes.c_long)]