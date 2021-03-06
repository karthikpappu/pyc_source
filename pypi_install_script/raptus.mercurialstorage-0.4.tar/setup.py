from setuptools import setup, find_packages
import os

version = '0.4'

setup(name='raptus.mercurialstorage',
      version=version,
      description="provides an archetypes storage which stores files on the filesystem into a mercurial repository",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone archetypes storage mercurial',
      author='Raptus AG',
      author_email='skaeser@raptus.com',
      url='http://plone.org/products/raptus.mercurialstorage',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['raptus'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.ExternalStorage',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
