from os.path import abspath, dirname, join
try:
  # try to use setuptools
  from setuptools import setup
  setupArgs = dict(
      include_package_data=True,
      install_requires=[] ,
      namespace_packages=['dm', 'dm.zodb'],
      zip_safe=False,
      test_requires=['zodb.repair'],
      )
except ImportError:
  # use distutils
  from distutils import setup
  setupArgs = dict(
    )

cd = abspath(dirname(__file__))
pd = join(cd, 'dm', 'zodb', 'repair')

def pread(filename, base=pd): return open(join(base, filename)).read().rstrip()

setup(name='dm.zodb.repair',
      version=pread('VERSION.txt').split('\n')[0],
      description="ZODB: recover lost objects from a backup",
      long_description=pread('README.txt'),
      classifiers=[
#        'Development Status :: 3 - Alpha',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Framework :: Zope2',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        ],
      author='Dieter Maurer',
      author_email='dieter@handshake.de',
      url='http://pypi.python.org/pypi/dm.zodb.repair',
      packages=['dm', 'dm.zodb', 'dm.zodb.repair'],
      keywords='ZODB recovery',
      license='ZPL',
      **setupArgs
      )
