# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0rc5'
description = 'Integração do Portal Modelo com buscadores externos.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='interlegis.portalmodelo.buscadores',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='interlegis portalmodelo lexml search plone',
    author='Programa Interlegis',
    author_email='ti@interlegis.leg.br',
    url='https://github.com/interlegis/interlegis.portalmodelo.buscadores',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['interlegis', 'interlegis.portalmodelo'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'plone.app.portlets',
        'plone.app.upgrade',
        'plone.portlets',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'zope.i18nmessageid',
        'zope.interface',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.testing',
            'robotsuite',
            'zope.component',
        ],
    },
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
