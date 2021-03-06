"""
Pyramid-Igniter
---------------
An extension that bootstraps your app with class-based views and Twitter Bootstrap.

Documentation: https://github.com/tark-hidden/pyramid_igniter

Changelog
*********

0.2.4
-----
* Now I have Python 3.4.3 locally and 2.7.3 on my VDS and I can check it on both interpreters. Python3 functions have no func_dict object but __dict__ works fine. Who cares? No one told me about that. And... inspect.ismethod still works here but isfunction don't.


0.2.3
-----
* Py3 compatibility support. Sorry.


0.2.2
-----
* Fixed a bug in route_name. Holy hell!


0.2.1
-----
* Fixed a bug in assigning route_base variable.


0.2
---
* Added a method render to the IgniterView class. Rendering process needs some additional info about objects; now you can do some things more simpler.


0.1
---
Initial release.

"""
from setuptools import setup, find_packages

setup(
    name='pyramid-igniter',
    version='0.2.4',
    url='https://github.com/tark-hidden/pyramid_igniter',
    license='BSD',
    author='Tark',
    maintainer='Tark',
    author_email='tark.hidden@gmail.com',
    description='Flexible class-based views and Twitter Bootstrap for Pyramid',
    keywords="bootstrap pyramid igniter",
    long_description=__doc__,
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'pyramid'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]    
)