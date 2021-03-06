from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.2'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(name='julpyter',
      version=__version__,
      description='A python package which converts a jupyter notebook to a Galvanize Learn challenge',
      long_description=long_description,
      url='https://github.com/embanner/julpyter',
      download_url='https://github.com/embanner/julpyter/tarball/' + __version__,
      license='BSD',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
      ],
      keywords='',
      packages=find_packages(exclude=['docs', 'tests*']),
      include_package_data=True,
      author='Edward Banner',
      install_requires=install_requires,
      dependency_links=dependency_links,
      author_email='edward.banner@galvanize.com',
      entry_points={
        'nbconvert.exporters': ['learn = julpyter:LearnExporter'],
      },
)
