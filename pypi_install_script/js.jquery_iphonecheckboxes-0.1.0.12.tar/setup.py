from setuptools import setup, find_packages
import os

version = '0.1.0.12'

setup(name='js.jquery_iphonecheckboxes',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Raptus AG',
      author_email='dev@raptus.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['js'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
        'fanstatic',
        'setuptools',
        'js.jquery'
      ],
    entry_points={
        'fanstatic.libraries': [
            'iphonecheckboxes.js = js.jquery_iphonecheckboxes:library',
            ],
        },
      )
