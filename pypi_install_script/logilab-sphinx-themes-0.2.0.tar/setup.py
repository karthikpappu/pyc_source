# 'setup.py'
from setuptools import setup
import codecs

# Version info -- read without importing
_locals = {}
with open("logilab_sphinx_themes/_version.py") as fp:
    exec(fp.read(), None, _locals)
version = _locals["__version__"]


# README into long description
with codecs.open('README.rst', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='logilab-sphinx-themes',
    version=version,
    description='A Sphinx theme for Logilab docs',
    long_description=readme,
    author='Logilab',
    author_email='contact@logilab.fr',
    url='https://www.logilab.org/project/logilab-sphinx-themes',
    packages=['logilab_sphinx_themes'],
    include_package_data=True,
    entry_points={
        'sphinx.html_themes': [
            'logilab = logilab_sphinx_themes',
        ]
    },
    install_requires=['sphinx'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
        ],
)
