from setuptools import setup, find_packages
import os

version = '1.2.1'

setup(name='collective.blog.star',
      version=version,
      description="Blog suite for Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
        ],
      keywords='plone blog',
      author='Jarn AS',
      author_email='info@jarn.com',
      url='https://github.com/collective/collective.blog.star',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.blog'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.blog.feeds>=2.1',
          'collective.blog.portlets>=1.5',
          'collective.blog.view>=1.5.2',
          'collective.twitterportlet',
          'collective.flowplayer',
          'qi.portlet.TagClouds',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
