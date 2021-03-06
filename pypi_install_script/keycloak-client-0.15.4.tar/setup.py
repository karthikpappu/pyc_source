# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='keycloak-client',
    version='0.15.4',
    url='https://github.com/ly798/python-keycloak.git',
    license='The MIT License',
    author='liuyang',
    author_email='liuyang@gmail.com',
    keywords='keycloak openid',
    description=u'keycloak-client(fork from python-keycloak) is a Python package providing access to the Keycloak API.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['keycloak', 'keycloak.authorization', 'keycloak.tests'],
    install_requires=['requests>=2.18.4', 'python-jose>=1.4.0'],
    tests_require=['httmock>=1.2.5'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Utilities'
    ]
)
