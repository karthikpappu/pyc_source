# restapi setup.py script
#
# It doesn't depend on setuptools, but if setuptools is available it'll use
# some of its features, like package dependencies.

from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES
from subprocess import Popen, PIPE
import os
import sys

PACKAGE = "taskpool"

class osx_install_data(install_data):
    # On MacOS, the platform-specific lib dir is /System/Library/Framework/Python/.../
    # which is wrong. Python 2.5 supplied with MacOS 10.5 has an Apple-specific fix
    # for this in distutils.command.install_data#306. It fixes install_lib but not
    # install_data, which is why we roll our own install_data class.

    def finalize_options(self):
        # By the time finalize_options is called, install.install_lib is set to the
        # fixed directory, so we set the installdir to install_lib. The
        # install_data class uses ('install_data', 'install_dir') instead.
        self.set_undefined_options('install', ('install_lib', 'install_dir'))
        install_data.finalize_options(self)

if sys.platform == "darwin":
    cmdclasses = {'install_data': osx_install_data}
else:
    cmdclasses = {'install_data': install_data}

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)

def is_not_module(filename):
    return os.path.splitext(filename)[1] not in ['.py', '.pyc', '.pyo']

for scrapy_dir in [PACKAGE]:
    for dirpath, dirnames, filenames in os.walk(scrapy_dir):
        # Ignore dirnames that start with '.'
        for i, dirname in enumerate(dirnames):
            if dirname.startswith('.'): del dirnames[i]
        if '__init__.py' in filenames:
            packages.append('.'.join(fullsplit(dirpath)))
            data = [f for f in filenames if is_not_module(f)]
            if data:
                data_files.append([dirpath, [os.path.join(dirpath, f) for f in data]])
        elif filenames:
            data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

# Small hack for working with bdist_wininst.
# See http://mail.python.org/pipermail/distutils-sig/2004-August/004134.html
if len(sys.argv) > 1 and sys.argv[1] == 'bdist_wininst':
    for file_info in data_files:
        file_info[0] = '\\PURELIB\\%s' % file_info[0]

with open(os.path.join(os.path.dirname(__file__), '{0}/version.py'.format(PACKAGE))) as f:
    version = f.read().strip().split()[-1]

_SITE = 'http://github.com/xgfone/{0}'.format(PACKAGE)
setup_args = {
    'name': PACKAGE,
    'version': version,
    'url': _SITE,
    'description': 'A task pool, execute tasks in the thread pool or the process pool',
    'long_description': 'Reference: {0}'.format(_SITE),
    'author': 'xgfone',
    'author_email': 'xgfone@126.com',
    'license': 'BSD',
    'packages': packages,
    'cmdclass': cmdclasses,
    'data_files': data_files,
    'include_package_data': True,
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
else:
    setup_args['install_requires'] = [
    ]

setup(**setup_args)
