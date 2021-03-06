from __future__ import print_function, division, absolute_import
"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup
from setuptools.command.build_py import build_py

import sys
import os
from distutils import log

exe_exts = os.environ.get('PATHEXT', "")
if sys.platform == 'win32':
    exe_exts = exe_exts.split(";")
else:
    exe_exts = exe_exts.split(":")


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def which(program):
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
            for ext in exe_exts:
                if is_exe(exe_file + ext):
                    return exe_file + ext
    return None


class build_pyqt4(build_py):
    user_options = (build_py.user_options +
                    [('rcc=', 'r', 'Program used to compile Qt resource files into python module'),
                     ('uic=', 'u', 'Program used to compile Qt UI files into python module')])

    def initialize_options(self):
        build_py.initialize_options(self)
        self.rcc = None
        self.uic = None

    def finalize_options(self):
        build_py.finalize_options(self)
        self.ensure_filename('rcc')
        self.ensure_filename('uic')

        if self.rcc is None:
            self.rcc = which('pyrcc4')
            if self.rcc is None:
                self.rcc = which('pyrcc')
            if self.rcc is None:
                raise RuntimeError("Error, cannot find pyrcc program")
        if self.uic is None:
            self.uic = which('pyuic4')
            if self.uic is None:
                self.uic = which('pyuic')
            if self.uic is None:
                raise RuntimeError("Error, cannot find pyuic program")

    def run(self):
        build_py.run(self)
        if not self.dry_run:
            print("files = {}".format(self.data_files))
            for package, src_dir, build_dir, files in self.data_files:
                new_files = []
                for f in files:
                    nf = self.make_module(src_dir, build_dir, f)
                    if nf is not None:
                        new_files.append(nf)
                files.extend(new_files)

    def make_module(self, src, pth, name):
        if name.endswith(".ui"):
            return self.make_ui(src, pth, name)
        elif name.endswith(".qrc"):
            return self.make_rc(src, pth, name)

    def make_ui(self, src, pth, name):
        src_file = os.path.join(src, name)
        new_name = "ui_{0}.py".format(name[:-3])
        dst_file = os.path.join(pth, new_name)
        cmd = [self.uic, '--from-imports', '-o', dst_file, src_file]
        log.info('Compile UI file "{0}" into "{1}"'.format(name, dst_file))
        self.spawn(cmd)
        return new_name

    def make_rc(self, src, pth, name):
        src_file = os.path.join(src, name)
        new_name = "{0}_rc.py".format(name[:-4])
        dst_file = os.path.join(pth, new_name)
        if sys.version_info.major == 2:
            ver = '-py2'
        else:
            ver = '-py3'
        cmd = [self.rcc, ver, '-o', dst_file, src_file]
        log.info('Compile RC file "{0}" into "{1}"'.format(name, dst_file))
        self.spawn(cmd)
        return new_name


setup(name='point-tracker',
      description='Track points and cells on 2D tissues over time.',
      long_description=open('README.txt').read(),
      author='Pierre Barbier de Reuille',
      author_email='pierre.barbierdereuille@gmail.com',
      packages=['point_tracker', 'point_tracker.tissue_plot'],
      package_data={'point_tracker': ['*.ui', '*.qrc', '*.png'],
                    'point_tracker.tissue_plot': ['*.ui', '*.qrc']},
      version="0.7.12",
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: X11 Applications :: Qt',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
                   'Natural Language :: English',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Scientific/Engineering :: Visualization',
                   ],
      platforms=['Linux', 'Windows', 'MacOS'],
      license='LICENSE',
      install_requires=['numpy >=1.5.0',
                        'scipy >=0.10.0',
                        'matplotlib',
                        'scikit-image'
                        ],
      url=['https://github.com/PierreBdR/point_tracker'],
      entry_points={
          'console_scripts': ['track_color = point_tracker.track_color:main'],
          'gui_scripts': ['point_tracker = point_tracker.tracking:main']},
      test_suite="nose.collector",
      tests_require="nose",
      cmdclass={'build_py': build_pyqt4},
      )
