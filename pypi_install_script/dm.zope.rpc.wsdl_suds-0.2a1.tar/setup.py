from os.path import abspath, dirname, join
try:
  # try to use setuptools
  from setuptools import setup
  setupArgs = dict(
      include_package_data=True,
      install_requires=[
        'setuptools', # to make "buildout" happy
        'dm.zope.rpc >= 0.2a1',
        'suds >= 0.3.9',
      ] ,
      namespace_packages=['dm', 'dm.zope', 'dm.zope.rpc'],
      zip_safe=False,
      entry_points = dict(
        ),
      )
except ImportError:
  # use distutils
  from distutils import setup
  setupArgs = dict(
    )

cd = abspath(dirname(__file__))
pd = join(cd, 'dm', 'zope', 'rpc', 'wsdl_suds')

def pread(filename, base=pd): return open(join(base, filename)).read().rstrip()


setup(name='dm.zope.rpc.wsdl_suds',
      version=pread('VERSION.txt').split('\n')[0],
      description="WSDL described SOAP protocol support for \"dm.zope.rpc\", based on \"suds\"",
      long_description=pread('README.txt'),
      classifiers=[
        'Development Status :: 3 - Alpha',
#        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Framework :: Zope2',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.6',
        'Topic :: Utilities',
        ],
      author='Dieter Maurer',
      author_email='dieter@handshake.de',
      url='http://pypi.python.org/pypi/dm.zope.rpc',
      packages=['dm', 'dm.zope', 'dm.zope.rpc',
                'dm.zope.rpc.wsdl_suds',
                ],
      license='BSD',
      keywords='rpc zope multiprotocol soap wsdl',
      **setupArgs
      )
