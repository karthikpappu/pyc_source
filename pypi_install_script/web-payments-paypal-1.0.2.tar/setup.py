#!/usr/bin/env python3
from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import sys

PACKAGES = [
    'web_payments_paypal']

REQUIREMENTS = [
    'web-payments-connector>=2.3.3<4.0a',
    'requests>=2.16.0',
    'simplejson'
]

TEST_REQUIREMENTS = [
    'pytest'
]

VERSIONING = {
    'root': '.',
    'version_scheme': 'guess-next-dev',
    'local_scheme': 'dirty-tag',
}


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    test_args = []

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
      name='web-payments-paypal',
      license="BSD3",
      author='Alexander Kaftan',
      author_email='devkral@web.de',
      description='Paypal plugin for web-payments-connector',
      use_scm_version=VERSIONING,
      setup_requires=['setuptools_scm'],
      url='http://github.com/devkral/web-payments-paypal',
      packages=PACKAGES,
      include_package_data=True,
      classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'],
      install_requires=REQUIREMENTS,
      cmdclass={
        'test': PyTest},
      tests_require=TEST_REQUIREMENTS,
      zip_safe=True)
