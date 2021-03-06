import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'docs', 'source', 'README.rst')).read()
CHANGES = open(os.path.join(here, 'docs', 'source', 'CHANGES.rst')).read()

requires = [
    'setuptools',
    'logbook',
    'lxml',
    'fs<1',
    'boto',
]

tests_requires = [
    'pytest',
]

setup(name='pp.core',
      version='0.4.4',
      description='pp.core',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
      ],
      author='Andreas Jung',
      author_email='info@zopyx.com',
      url='http://pypi.python.org/pypi/pp.core',
      keywords='Python Produce & Publish',
      packages=['pp', 'pp.core'],
      include_package_data=True,
      zip_safe=False,
      namespace_packages=['pp'],
      install_requires=requires,
      tests_require=tests_requires,
      test_suite="pp.portal",
      extras_require={
          'testing': tests_requires,
      },
      entry_points="""\
      """,
      )
