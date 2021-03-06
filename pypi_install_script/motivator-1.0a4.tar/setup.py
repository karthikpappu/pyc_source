from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '1.0a4'

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'pyttsx'
]


setup(name='motivator',
      version=version,
      description="Motivate oneself with a phrase that can be repeated",
      long_description=README + '\n\n' + NEWS,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='srid',
      author_email='srid@nearfar.org',
      url='http://bitbucket.org/srid/motivator',
      license='MIT',
      packages=find_packages('src'),
      package_dir = {'': 'src'},include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points={
          'console_scripts': ['motivator=motivator:main']
      }
      )
