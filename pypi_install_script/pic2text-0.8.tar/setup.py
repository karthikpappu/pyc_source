from setuptools import setup
setup(
  name = 'pic2text',
  packages = ['pic2text'], # this must be the same as the name above
  version = '0.8',
  description = 'A small tool that converts photos to semi-readable/viewable strings and then pastes them in the cmd-line or outputs a txt file',
  author = 'Spencer Judd',
  author_email = 'spencerjfam@gmail.com',
  url = 'https://github.com/STJudd109/pic2text', # use the URL to the github repo
  download_url = 'https://github.com/STJudd109/pic2text/archive/v0.8.tar.gz', # I'll explain this in a second
  keywords = ['picture', 'commandline', 'silly'], # arbitrary keywords
  classifiers = [],
  install_requires=[
          'pillow',
          'requests'
      ],
  entry_points={
      'console_scripts': [
                'pic2text=pic2text.__main__:main',
            ],
        },
)

# """A samll picture to text tool.
# See:
# https://github.com/STJudd109/pic2text
# """

# # Always prefer setuptools over distutils
# from setuptools import setup, find_packages
# # To use a consistent encoding
# from codecs import open
# from os import path

# here = path.abspath(path.dirname(__file__))

# setup(
#     name='pic2text',

#     # Versions should comply with PEP440.  For a discussion on single-sourcing
#     # the version across setup.py and the project code, see
#     # https://packaging.python.org/en/latest/single_source_version.html
#     version='0.3',

#     description='A samll picture to text tool',
#     long_description="A small tool that converts photos to semi-readable/viewable strings and then pastes them in the cmd-line or outputs a txt file",

#     # The project's main homepage.
#     url='https://github.com/STJudd109/pic2text',

#     # Author details
#     author='Spencer Judd',
#     author_email='spencerjfam@gmail.com',

#     # Choose your license
#     license='MIT',

#     # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
#     classifiers=[
#         # How mature is this project? Common values are
#         #   3 - Alpha
#         #   4 - Beta
#         #   5 - Production/Stable
#         'Development Status :: 3 - Alpha',

#         # Indicate who your project is intended for
#         'Intended Audience :: Developers',
#         'Topic :: random :: tools',

#         # Pick your license as you wish (should match "license" above)
#         'License :: OSI Approved :: MIT License',

#         # Specify the Python versions you support here. In particular, ensure
#         # that you indicate whether you support Python 2, Python 3 or both.
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.3',
#         'Programming Language :: Python :: 3.4',
#         'Programming Language :: Python :: 3.5',
#     ],

#     # What does your project relate to?
#     keywords='silly pictures tools',

#     # You can just specify the packages manually here if your project is
#     # simple. Or you can use find_packages().
#     packages=find_packages(exclude=['contrib', 'docs', 'tests']),

#     # Alternatively, if you want to distribute just a my_module.py, uncomment
#     # this:
#     #   py_modules=["my_module"],

#     # List run-time dependencies here.  These will be installed by pip when
#     # your project is installed. For an analysis of "install_requires" vs pip's
#     # requirements files see:
#     # https://packaging.python.org/en/latest/requirements.html
#     install_requires=['pillow'],

#     # List additional groups of dependencies here (e.g. development
#     # dependencies). You can install these using the following syntax,
#     # for example:
#     # $ pip install -e .[dev,test]

#     # If there are data files included in your packages that need to be
#     # installed, specify them here.  If using Python 2.6 or less, then these
#     # have to be included in MANIFEST.in as well.
#     # package_data={
#     #     'sample': ['package_data.dat'],
#     # },

#     # Although 'package_data' is the preferred approach, in some case you may
#     # need to place data files outside of your packages. See:
#     # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
#     # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
#     # data_files=[('my_data', ['data/data_file'])],

#     # To provide executable scripts, use entry points in preference to the
#     # "scripts" keyword. Entry points provide cross-platform support and allow
#     # pip to create the appropriate form of executable for the target platform.
#     entry_points={
#         'console_scripts': [
#             'pic2text=pic2text:main',
#         ],
#     },
# )