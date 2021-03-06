from distutils.core import setup

import glob
import os

VERSION = '0.1.6'

setup(
    name='mimey3000',
    version=VERSION,
    description="RESTful mime handling plugin for Pyramid",
    long_description="""
    RESTful mime handling plugin for Pyramid.
    Provides tools that will handle serialization and
    deserialization of objects depending on standard HTTP headers.
    """,
    author='John-John Tedro',
    author_email='johnjohn.tedro@gmail.com',
    url='http://github.com/ron-burgundy1/mimeprovider',
    license='GPLv3',
    data_files=[
        ("examples", glob.glob(os.path.join("examples", "*.py")))
    ],
    packages=[
        'mimeprovider',
        'mimeprovider.validators',
        'mimeprovider.packages',
        'mimeprovider.documenttype',
        'mimeprovider.client',
    ],
)
