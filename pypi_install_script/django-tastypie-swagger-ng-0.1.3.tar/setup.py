#!/usr/bin/env python

from setuptools import setup
import tastypie_swagger

description = "An adapter to use swagger-ui with django-tastypie"

try:
    longdesc = open('README.rst').read()
except Exception:
    longdesc = description

setup(
    # Metadata
    name='django-tastypie-swagger-ng',
    version='.'.join(map(str, tastypie_swagger.VERSION)),
    description=description,
    long_description=longdesc,
    author='ifanr',
    author_email='adamwen@ifanr.com',
    classifiers=[
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
    url='https://github.com/ifanrx/django-tastypie-swagger',
    download_url='https://github.com/ifanrx/django-tastypie-swagger/downloads',
    license='BSD',
    packages=['tastypie_swagger'],
    include_package_data=True,
    zip_safe=False,
)
