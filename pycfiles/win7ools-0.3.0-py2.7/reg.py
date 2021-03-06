# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\win7ools\reg.py
# Compiled at: 2014-12-26 18:14:34
"""Registry key values and functions for working with Windows registry.

***KEY_user_assist uses HKCU***
***KEY_py_runas_admin uses HKCR***
***KEY_installer uses HKCR***
***KEY_DisplayFusion uses HKCU***
***KEY_drives uses HKLM and HKCU***
***KEY_classes uses HKCR***
***KEY_folders uses HKLM***
"""
import codecs
from datetime import datetime
import os, os.path as path, _winreg as reg
from distutils.log import warn
import re, string
from subprocess import call
from win7ools.lib import hex_to_str as h2s
UMWE = 11644473600
LOCAL_MACHINE = reg.HKEY_LOCAL_MACHINE
CLASSES_ROOT = reg.HKEY_CLASSES_ROOT
CURRENT_USER = reg.HKEY_CURRENT_USER
ALL_ACCESS = reg.KEY_ALL_ACCESS
READ = reg.KEY_READ
WOW64 = reg.KEY_WOW64_64KEY

class RegistryKeys(object):
    """
    Registry key values

    ***user_assist uses HKCU***
    ***py_runas_admin uses HKCR***
    ***installer uses HKCR***
    ***DisplayFusion uses HKCU***
    ***drives uses HKLM and HKCU***
    ***classes uses HKCR***
    ***folders uses HKLM***
    """

    def __init__(self):
        self.microsoft = 'Software\\Microsoft'
        self.windows = self.microsoft + '\\Windows'
        self.windowsNT = self.microsoft + '\\Windows NT'
        self.microsoft64 = 'Software\\Wow6432Node\\Microsoft'
        self.windows64 = self.microsoft64 + '\\Windows'
        self.current_version = self.windows + '\\CurrentVersion'
        self.last_regedit = self.current_version + '\\Applets'
        self.usb = 'SYSTEM\\CurrentControlSet\\Enum\\USB'
        self.usb_store = 'SYSTEM\\CurrentControlSet\\Enum\\USBSTOR'
        self.session_manager = 'SYSTEM\\CurrentControlSet\\Control\\Session Manager'
        self.classes = '\\CLSID'
        self.user_assist = self.current_version + '\\Explorer\\UserAssist'
        self.folders = self.current_version + '\\Explorer\\FolderDescriptions'
        self.logon = self.current_version + '\\Authentication\\LogonUI\\Background'
        self.uninstall = self.current_version + '\\Uninstall'
        self.runas_admin = 'Python.File\\shell\\runas'
        self.uninstall_wow6432 = '%s\\CurrentVersion\\Uninstall' % self.windows64
        self.installer = '\\Installer\\Products'
        self.DisplayFusion = 'Software\\Binary Fortress Software'
        self.drives = 'Software\\Classes\\Applications\\Explorer.exe\\Drives'
        self.TRIM = self.session_manager + '\\Memory Management\\PrefetchParameters'
        self.environment = self.session_manager + '\\Environment'
        self.sid = self.windowsNT + '\\CurrentVersion\\ProfileList'
        self.masterkey = self.microsoft + '\\Cryptography\\Protect\\Providers'

    def __getitem__(self, key):
        return self.__dict__[key]

    def key(self, value):
        """
        return key from registry value and return
        """
        return 'under construction'


def save_key(keyStr, exportPath, HKLM=True, HKCU=False, HKCR=False):
    """
    Export key named keyStr to REG file, exportPath.
    
    ***REQUIRES ADMINISTRATOR PRIVILEGES***    
    """
    if os.path.exists(exportPath):
        os.remove(exportPath)
    if HKLM:
        keyPath = 'HKEY_LOCAL_MACHINE\\' + keyStr
    if HKCU:
        keyPath = 'HKEY_CURRENT_USER\\' + keyStr
    if HKCR:
        keyPath = 'HKEY_CLASSES_ROOT\\' + keyStr
    keyPath = '"%s"' % keyPath
    exportPath = '"%s"' % exportPath
    cmd = 'reg export ' + keyPath + ' ' + exportPath
    print cmd
    try:
        call(cmd, shell=True)
        return True
    except:
        warn('Failed to execute ' + cmd)
        return False


def get_values(keyStr, HKCU=False, HKCR=False):
    """
    keyStr is string name of key to get subkey values from
    Default base key is HKEY_LOCAL_MACHINE.  
    To use HKEY_CURRENT_USER, set HKCU=True.
    Has READ access, not meant for editing keys.
    Returns a JSON-like object for future export. For example,
    
    get_values(RegistryKeys().uninstall) will return:
    [
        {
            'RegistryName': <name of uninstall subkey for software>,
            'Subkeys':
            {
                'DisplayName': <sometimes does not exist>,
                'DisplayVersion': <sometimes does not exist>,
                'InstallLocation': <sometimes does not exist>,
                .
                .
                .
            }
        },...
    ]"""
    keyList = []
    if HKCU:
        parentKey = CURRENT_USER
    if HKCR:
        parentKey = CLASSES_ROOT
    if not HKCU and not HKCR:
        parentKey = LOCAL_MACHINE
    try:
        with reg.ConnectRegistry(None, parentKey) as (x):
            with reg.OpenKey(x, keyStr, 0, READ | WOW64) as (key):
                keyNumber = reg.QueryInfoKey(key)[0]
                keyList = [''] * keyNumber
                if keyNumber >= 1:
                    for i in range(0, keyNumber):
                        regName = reg.EnumKey(key, i)
                        with reg.OpenKey(key, regName, 0, READ | WOW64) as (sub):
                            keyList[i] = {'RegistryName': regName, 'Values': {}}
                            for j in range(0, reg.QueryInfoKey(sub)[1]):
                                val = reg.EnumValue(sub, j)
                                keyList[i]['Values'].update({val[0]: val[1]})

                else:
                    regName = path.basename(keyStr)
                    keyList = {'RegistryName': regName, 'Values': {}}
                    for i in range(0, reg.QueryInfoKey(key)[1]):
                        val = reg.EnumValue(key, i)
                        keyList['Values'].update({val[0]: val[1]})

    except:
        warn('Failed to load %s' % keyStr)

    return keyList


def get_sid(keys=RegistryKeys()):
    """Get SID for current user."""
    import getpass
    user = getpass.getuser()
    for i in get_values(keys.sid):
        for j in i['Values'].items():
            try:
                if user in j[1]:
                    return i['RegistryName']
            except:
                pass


def get_masterkey_guid(keys=RegistryKeys()):
    return get_values(keys.masterkey)[0]['RegistryName']


def get_clsid_dict(keys=RegistryKeys()):
    clsid_dict = {}
    paths = {'ProgramFilesX86': os.environ['PROGRAMFILES(X86)'], 'ProgramFilesX64': os.environ['PROGRAMW6432'], 
       'System': os.environ['SYSTEMROOT'] + '\\System32', 
       'SystemX86': os.environ['SYSTEMROOT'] + '\\System32', 
       'Windows': os.environ['SYSTEMROOT']}
    for clsid in get_values(keys.classes, HKCR=True):
        GUID = clsid['RegistryName'].upper()
        try:
            try:
                name = clsid['Values']['']
                try:
                    name = paths[name]
                except:
                    pass

            except:
                name = ''

        finally:
            clsid_dict.update({GUID: name})

    for clsid in get_values(keys.folders):
        GUID = clsid['RegistryName'].upper()
        try:
            try:
                name = clsid['Values']['Name']
                try:
                    name = paths[name]
                except:
                    pass

            except:
                name = ''

        finally:
            clsid_dict.update({GUID: name})

    return clsid_dict


def FILETIME_to_datetime(filetime):
    """
    Converts a Microsoft FILETIME time to a standard datetime object.
    <filetime> should be a list of hex values.  If list is taken directly
    from registry, it should be reversed before inputted to this function
    as FILETIMEs are stored in the "little endian" format.
    """
    filetime = string.join([ h2s(i) for i in filetime ])
    filetime = re.sub(' ', '', filetime)
    filetime = long(filetime, base=16) / 10000000.0
    filetime = filetime - UMWE if filetime > UMWE else filetime
    return datetime.fromtimestamp(filetime)


def get_user_assist(keys=RegistryKeys()):
    """
    Returns decrypted list of items in HKCU UserAssist.
    - Converts FILETIME times to standard UNIX time
    - Decrypts program names with ROT-13
    - Returns list of dictionaries:
        [
            {
                'value': <program name>},
                'count': <number of times program was run>,
                'lastrun': <date that program was run last>,
                'data': <extra registry data...just in case>
            }
        ]
    """
    userassist = []
    clsid_dict = get_clsid_dict()
    for key in get_values(keys.user_assist, HKCU=True):
        keyname = '%s\\%s' % (keys.user_assist, key['RegistryName'])
        for val in get_values(keyname, HKCU=True)[0]['Values']:
            data = []
            valname = '%s\\%s' % (keyname, 'Count')
            with reg.ConnectRegistry(None, CURRENT_USER) as (x):
                with reg.OpenKey(x, valname) as (value):
                    val_data = reg.QueryValueEx(value, val)[0]
                    for i in val_data:
                        data.append(hex(ord(i)))

            count = string.join([ str(i) for i in data[4:8][::-1] ])
            count = re.sub(' ', '', re.sub('x', '', count))
            count = int(count, base=16)
            lastrun = FILETIME_to_datetime(data[60:68][::-1])
            try:
                ua_value = clsid_dict[codecs.decode(val, 'rot_13')]
            except:
                ua_value = codecs.decode(val, 'rot_13')

            m = re.match('[{].*[}]', ua_value)
            if m:
                clsid = m.group()
                try:
                    ua_value = re.sub(clsid, clsid_dict[clsid], ua_value)
                except:
                    pass

            userassist.append({'value': ua_value, 'count': count, 
               'lastrun': lastrun, 
               'data': data})

    return userassist