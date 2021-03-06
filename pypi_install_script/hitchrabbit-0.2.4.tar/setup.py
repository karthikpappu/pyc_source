# -*- coding: utf-8 -*
from setuptools.command.install import install
from setuptools import find_packages
from setuptools import setup
import subprocess
import codecs
import sys
import os


def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), 'r').read()

setup(name="hitchrabbit",
      version="0.2.4",
      description="Plugin to run RabbitMQ using the Hitch testing framework.",
      long_description=read('README.rst'),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities',
          'Environment :: Console',
          'Topic :: Database',
          'Operating System :: Unix',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
      keywords='hitch testing framework bdd tdd declarative tests testing service rabbitmq rabbit database',
      author='Colm O\'Connor',
      author_email='colm.oconnor.github@gmail.com',
      url='https://hitchtest.readthedocs.org/',
      license='AGPL',
      install_requires=['hitchserve', 'hitchtest', ],
      packages=find_packages(exclude=[]),
      package_data={},
      zip_safe=False,
      include_package_data=True,
)
