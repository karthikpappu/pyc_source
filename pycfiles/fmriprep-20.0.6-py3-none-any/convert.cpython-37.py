# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/wheel/wheel/cli/convert.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 9498 bytes
import os.path, re, shutil, sys, tempfile, zipfile
from distutils import dist
from glob import iglob
from ..bdist_wheel import bdist_wheel
from ..wheelfile import WheelFile
from . import WheelError, require_pkgresources
egg_info_re = re.compile('\n    (?P<name>.+?)-(?P<ver>.+?)\n    (-(?P<pyver>py\\d\\.\\d+)\n     (-(?P<arch>.+?))?\n    )?.egg$', re.VERBOSE)

class _bdist_wheel_tag(bdist_wheel):
    full_tag_supplied = False
    full_tag = None

    def get_tag(self):
        if self.full_tag_supplied:
            if self.full_tag is not None:
                return self.full_tag
        return bdist_wheel.get_tag(self)


def egg2wheel(egg_path, dest_dir):
    filename = os.path.basename(egg_path)
    match = egg_info_re.match(filename)
    if not match:
        raise WheelError('Invalid egg file name: {}'.format(filename))
    else:
        egg_info = match.groupdict()
        dir = tempfile.mkdtemp(suffix='_e2w')
        if os.path.isfile(egg_path):
            with zipfile.ZipFile(egg_path) as (egg):
                egg.extractall(dir)
        else:
            for pth in os.listdir(egg_path):
                src = os.path.join(egg_path, pth)
                if os.path.isfile(src):
                    shutil.copy2(src, dir)
                else:
                    shutil.copytree(src, os.path.join(dir, pth))

        pyver = egg_info['pyver']
        if pyver:
            pyver = egg_info['pyver'] = pyver.replace('.', '')
        arch = (egg_info['arch'] or 'any').replace('.', '_').replace('-', '_')
        abi = 'cp' + pyver[2:] if arch != 'any' else 'none'
        root_is_purelib = egg_info['arch'] is None
        if root_is_purelib:
            bw = bdist_wheel(dist.Distribution())
        else:
            bw = _bdist_wheel_tag(dist.Distribution())
    bw.root_is_pure = root_is_purelib
    bw.python_tag = pyver
    bw.plat_name_supplied = True
    bw.plat_name = egg_info['arch'] or 'any'
    if not root_is_purelib:
        bw.full_tag_supplied = True
        bw.full_tag = (pyver, abi, arch)
    dist_info_dir = os.path.join(dir, ('{name}-{ver}.dist-info'.format)(**egg_info))
    bw.egg2dist(os.path.join(dir, 'EGG-INFO'), dist_info_dir)
    bw.write_wheelfile(dist_info_dir, generator='egg2wheel')
    wheel_name = ('{name}-{ver}-{pyver}-{}-{}.whl'.format)(abi, arch, **egg_info)
    with WheelFile(os.path.join(dest_dir, wheel_name), 'w') as (wf):
        wf.write_files(dir)
    shutil.rmtree(dir)


def parse_wininst_info(wininfo_name, egginfo_name):
    """Extract metadata from filenames.

    Extracts the 4 metadataitems needed (name, version, pyversion, arch) from
    the installer filename and the name of the egg-info directory embedded in
    the zipfile (if any).

    The egginfo filename has the format::

        name-ver(-pyver)(-arch).egg-info

    The installer filename has the format::

        name-ver.arch(-pyver).exe

    Some things to note:

    1. The installer filename is not definitive. An installer can be renamed
       and work perfectly well as an installer. So more reliable data should
       be used whenever possible.
    2. The egg-info data should be preferred for the name and version, because
       these come straight from the distutils metadata, and are mandatory.
    3. The pyver from the egg-info data should be ignored, as it is
       constructed from the version of Python used to build the installer,
       which is irrelevant - the installer filename is correct here (even to
       the point that when it's not there, any version is implied).
    4. The architecture must be taken from the installer filename, as it is
       not included in the egg-info data.
    5. Architecture-neutral installers still have an architecture because the
       installer format itself (being executable) is architecture-specific. We
       should therefore ignore the architecture if the content is pure-python.
    """
    egginfo = None
    if egginfo_name:
        egginfo = egg_info_re.search(egginfo_name)
        if not egginfo:
            raise ValueError('Egg info filename %s is not valid' % (egginfo_name,))
    w_name, sep, rest = wininfo_name.partition('-')
    if not sep:
        raise ValueError('Installer filename %s is not valid' % (wininfo_name,))
    rest = rest[:-4]
    rest2, sep, w_pyver = rest.rpartition('-')
    if sep and w_pyver.startswith('py'):
        rest = rest2
        w_pyver = w_pyver.replace('.', '')
    else:
        w_pyver = 'py2.py3'
    w_ver, sep, w_arch = rest.rpartition('.')
    if not sep:
        raise ValueError('Installer filename %s is not valid' % (wininfo_name,))
    if egginfo:
        w_name = egginfo.group('name')
        w_ver = egginfo.group('ver')
    return {'name':w_name,  'ver':w_ver,  'arch':w_arch,  'pyver':w_pyver}


def wininst2wheel(path, dest_dir):
    with zipfile.ZipFile(path) as (bdw):
        egginfo_name = None
        for filename in bdw.namelist():
            if '.egg-info' in filename:
                egginfo_name = filename
                break

        info = parse_wininst_info(os.path.basename(path), egginfo_name)
        root_is_purelib = True
        for zipinfo in bdw.infolist():
            if zipinfo.filename.startswith('PLATLIB'):
                root_is_purelib = False
                break

        if root_is_purelib:
            paths = {'purelib': ''}
        else:
            paths = {'platlib': ''}
        dist_info = '%(name)s-%(ver)s' % info
        datadir = '%s.data/' % dist_info
        members = []
        egginfo_name = ''
        for zipinfo in bdw.infolist():
            key, basename = zipinfo.filename.split('/', 1)
            key = key.lower()
            basepath = paths.get(key, None)
            if basepath is None:
                basepath = datadir + key.lower() + '/'
            else:
                oldname = zipinfo.filename
                newname = basepath + basename
                zipinfo.filename = newname
                del bdw.NameToInfo[oldname]
                bdw.NameToInfo[newname] = zipinfo
                if newname:
                    members.append(newname)
                if egginfo_name or newname.endswith('.egg-info'):
                    egginfo_name = newname
            if '.egg-info/' in newname:
                egginfo_name, sep, _ = newname.rpartition('/')

        dir = tempfile.mkdtemp(suffix='_b2w')
        bdw.extractall(dir, members)
    abi = 'none'
    pyver = info['pyver']
    arch = (info['arch'] or 'any').replace('.', '_').replace('-', '_')
    if root_is_purelib:
        arch = 'any'
    else:
        if arch != 'any':
            pyver = pyver.replace('py', 'cp')
        wheel_name = '-'.join((dist_info, pyver, abi, arch))
        if root_is_purelib:
            bw = bdist_wheel(dist.Distribution())
        else:
            bw = _bdist_wheel_tag(dist.Distribution())
    bw.root_is_pure = root_is_purelib
    bw.python_tag = pyver
    bw.plat_name_supplied = True
    bw.plat_name = info['arch'] or 'any'
    if not root_is_purelib:
        bw.full_tag_supplied = True
        bw.full_tag = (pyver, abi, arch)
    dist_info_dir = os.path.join(dir, '%s.dist-info' % dist_info)
    bw.egg2dist(os.path.join(dir, egginfo_name), dist_info_dir)
    bw.write_wheelfile(dist_info_dir, generator='wininst2wheel')
    wheel_path = os.path.join(dest_dir, wheel_name)
    with WheelFile(wheel_path, 'w') as (wf):
        wf.write_files(dir)
    shutil.rmtree(dir)


def convert(files, dest_dir, verbose):
    require_pkgresources('wheel convert')
    for pat in files:
        for installer in iglob(pat):
            if os.path.splitext(installer)[1] == '.egg':
                conv = egg2wheel
            else:
                conv = wininst2wheel
            if verbose:
                print('{}... '.format(installer))
                sys.stdout.flush()
            conv(installer, dest_dir)
            if verbose:
                print('OK')