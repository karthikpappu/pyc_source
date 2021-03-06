# -*- coding: UTF-8 -*-
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
VERSION = "1.0.0"


if __name__ == "__main__":
    setup(
        name="VAPTCHA",
        version=VERSION,
        packages=['vaptchasdk'],
        url='https://github.com/vaptcha/vaptcha-python-sdk',
        license='',
        author='VAPTCHA',
        author_email='vaptcha@wlinno.com',
        description='VAPTCHA Python SDK',
    	)
