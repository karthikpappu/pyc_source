from codecs import open as _open
from os import path

from setuptools import setup

HERE = path.abspath(path.dirname(__file__))
VERSION = '0.1.0'
PACKAGE = 'haproxysubdomains'

with _open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

    setup(
        name=PACKAGE,
        version=VERSION,
        description='Manages redirect rules in haproxy configuration based on subdomain acl.',
        long_description=LONG_DESCRIPTION,
        author='Pierre Penninckx',
        author_email='ibizapeanut@gmail.com',
        license='GPLv3',
        packages=[PACKAGE.lower()],
        url='https://github.com/ibizaman/' + PACKAGE.lower(),
        download_url='https://github.com/ibizaman/{}/archive/{}.tar.gz'.format(PACKAGE.lower(), VERSION),
        keywords=['haproxy'],
        entry_points = {
            'console_scripts': ['{0}={0}.__main__:main'.format(PACKAGE.lower())],
        },
        install_requires=[
            'pyhaproxy == 0.3.6',
            'PyYAML == 3.12',
        ],
        extras_require={
            'dev': [
                'pylint == 1.7.2',
            ],
            'test': [
                'coverage == 4.4.1',
                'pytest == 3.1.3',
                'pytest-cov == 2.5.1',
            ],
        }
    )
