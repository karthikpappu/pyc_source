from setuptools import setup, find_packages

version = '0.1'

setup(name='inquant.contentmirror',
      version=version,
      description="mirror plone content transparently in a plone site",
      long_description=file("inquant/contentmirror/README.rst").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Stefan Eletzhofer',
      author_email='stefan.eletzhofer@inquant.de',
      url='https://svn.plone.org/svn/collective/inquant.contentmirror/trunk',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['inquant'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
