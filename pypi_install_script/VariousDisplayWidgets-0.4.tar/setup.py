# -*- coding: utf-8 -*-
"""
This module contains the tool of VariousDisplayWidgets
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.4'

long_description = (
    open(os.path.join("VariousDisplayWidgets",
                      "VariousDisplayWidgets",
                      "readme.txt")).read() + '\n\n' +\
    open(os.path.join("VariousDisplayWidgets",
                      "VariousDisplayWidgets",
                      "changes.txt")).read()
)

tests_require = ['zope.testing']

setup(name='VariousDisplayWidgets',
      version=version,
      description="Various usable displays of text content, for example URIs.",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['VariousDisplayWidgets', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='VariousDisplayWidgets.VariousDisplayWidgets.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
