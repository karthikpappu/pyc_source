try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import sys, os

version = '0.5.2'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    "PermissionKit\n"
    "+++++++++++++\n\n"
    ".. contents :: \n"
    "\n"+read('doc/index.txt')
    + '\n'
    + read('CHANGELOG.txt')
    + '\n'
    'License\n'
    '=======\n'
    + read('LICENSE.txt')
    + '\n'
    'Download\n'
    '========\n'
)

setup(
    name='PermissionKit',
    version=version,
    description="A very simple framework for creating permission objects and using them in authorization checks.",
    long_description=long_description,
    # Get classifiers from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python',
    ],
    keywords='',
    author='James Gardner',
    author_email='',
    url='',
    license='GPLv3',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    extras_require={
        'test': [],
    },
    entry_points="""
    """,
)
