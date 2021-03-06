import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-direct',
    version='0.7.8',
    packages=['direct', ],
    include_package_data=True,
    license='GPLv2',  
    description='A simple Django application that provides a RESTFul Direct certificate validation API.',
    long_description=README,
    url='https://github.com/videntity/django-direct',
    author='Alan Viars',
    author_email='sales@videntity.com',
    install_requires=[
        'getdc', 'Django<=1.8.6', 'django-widget-tweaks', 'django-bootstrap-form',
        'pyOpenSSL' ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
