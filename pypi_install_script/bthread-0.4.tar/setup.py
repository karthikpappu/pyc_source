from setuptools import setup, find_packages
import subprocess
import re

DEFAULT_VERSION = "0.0.0"


def convert_version(version):
    pattern = re.compile(
        r"^(?P<main>[0-9\.rvVR]+)(\-(?P<post>[0-9]+))?(\-.+)?$")
    ver = pattern.search(version)

    if not ver:
        return DEFAULT_VERSION

    new_ver = ver.group('main')

    if ver.group('post'):
        new_ver += ".post{}".format(ver.group('post'))

    return new_ver


try:
    version = subprocess.check_output(
            'git describe --tags', shell=True).rstrip().decode('utf-8')
except subprocess.CalledProcessError:
    version = DEFAULT_VERSION

setup(name='bthread',
      version=version,
      description='',
      url='https://github.com/cy-arduino/python_better_therad',
      author='ChihYing_Lin',
      author_email='',
      license='LGPL',
      packages=find_packages(exclude=['tests', 'test_*']),
      zip_safe=False)
