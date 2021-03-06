import sys
import os.path
from setuptools import setup, Extension, find_packages
from distutils.command.sdist import sdist as _sdist
from distutils.command.build_ext import build_ext as _build_ext

if sys.version_info[:2] < (3, 4):
    sys.stdout.write('Python 3.4 or later is required\n')
    sys.exit(1)


def no_cythonize(extensions, **_ignore):
    """Change .pyx to .c or .cpp (copied from Cython documentation)"""
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            path, ext = os.path.splitext(sfile)
            if ext in ('.pyx', '.py'):
                if extension.language == 'c++':
                    ext = '.cpp'
                else:
                    ext = '.c'
                sfile = path + ext
            sources.append(sfile)
        extension.sources[:] = sources


extensions = [
    Extension('alignlib._core', sources=['src/alignlib/_core.pyx']),
]


class BuildExt(_build_ext):
    def run(self):
        # If we encounter a PKG-INFO file, then this is likely a .tar.gz/.zip
        # file retrieved from PyPI that already includes the pre-cythonized
        # extension modules, and then we do not need to run cythonize().
        if os.path.exists('PKG-INFO'):
            no_cythonize(extensions)
        else:
            # Otherwise, this is a 'developer copy' of the code, and then the
            # only sensible thing is to require Cython to be installed.
            from Cython.Build import cythonize
            self.extensions = cythonize(self.extensions)
        super().run()


class SDist(_sdist):
    def run(self):
        # Make sure the compiled Cython files in the distribution are up-to-date
        from Cython.Build import cythonize
        cythonize(extensions)
        super().run()


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='alignlib',
    setup_requires=['setuptools_scm'],  # Support pip versions that don't know about pyproject.toml
    use_scm_version={'write_to': 'src/alignlib/_version.py'},
    author='Marcel Martin',
    author_email='marcel.martin@scilifelab.se',
    url='https://github.com/marcelm/alignlib/',
    description='Some sequence alignment routines',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    ext_modules=extensions,
    cmdclass={'build_ext': BuildExt, 'sdist': SDist},
    classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Programming Language :: Cython",
            "Programming Language :: Python :: 3",
            "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]
)
