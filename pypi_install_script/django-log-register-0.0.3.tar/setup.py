import os
from setuptools import setup
README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-log-register',
    version='0.0.3',
    packages=['log_register'],
    include_package_data=True,
    license='BSD License',
    description='A simple Django app to register log and save them.',
    long_description=README,
    url='https://github.com/lalo73/django-log-register',
    author='Leandro Gomez',
    author_email='leandro.gz73@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

__author__ = 'leandro'
