from setuptools import setup, find_packages
import os

version = '1.0a6'

setup(name='collective.wtforms',
      version=version,
      description="Plone wtforms integration",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='forms plone wtforms',
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='http://github.com/collective/collective.wtforms',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'WTForms',
          'unidecode'
      ],
      extras_require=dict(
          tests=['plone.app.testing']
      ),
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
