# MYBOT - MYBOT is a IRC bot you can program your own commands for
#
# setup.py

import importlib

from setuptools import setup

importlib.invalidate_caches()

def read():
    return open("README.rst", "r").read()

setup(
    name='mybot',
    version='2',
    url='https://bitbucket.org/botlib/mybot',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="MYBOT is a IRC bot you can program your own commands for. no copyright, noLICENSE, placed in the public domain.",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license='Public Domain',
    zip_safe=True,
    data_files=[("files", ("/mybot.service", ""))],
    packages=["mybot", "bot", "lo"],
    scripts=["bin/mybot"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
