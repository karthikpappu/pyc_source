###
### $Release: 0.7.2 $
### $Copyright: copyright(c) 2008-2012 kuwata-lab.com all rights reserved. $
### $License: MIT License $
###


import sys
arg1 = len(sys.argv) >= 2 and sys.argv[1] or None
if arg1 == 'sdist':
    # --force-manifest is not supported in setuptools
    from distutils.core import setup
else:
    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup


def _kwargs():
    name             = 'Kook'
    version          = '0.7.2'
    author           = 'makoto kuwata'
    author_email     = 'kwa@kuwata-lab.com'
    maintainer       = author
    maintainer_email = author_email
    url              = 'http://www.kuwata-lab.com/kook/'
    description      = 'task automation tool for Python, similar to Make, Rake, Ant, or Cook'
    long_description = r'''
pyKook is a very useful tool to control your task such as compile, install or clean.
pyKook is similar to Make, Rake, Ant, or Cook.
Kookbook.py, which is a task definition file for pyKook, is written in Python.

Simple Example of Kookbook.py::

    @recipe
    def hello(c):
        print("Hello")

Output Result::

    bash> kk hello     # or pykook hello
    ### * hello (recipe=hello)
    Hello

Other Example of Kookbook.py::

    CC = prop('CC', 'gcc -Wall')
    kookbook.default = 'all'

    @recipe
    @ingreds('hello')                      # ingredients
    def all(c):                            # or task_all(c)
        pass

    @recipe('*.o', ['$(1).c', '$(1).h'])   # @recipe(product, [ingredients])
    def file_o(c):
        """compile *.c and *.h into *.o"""
        system(c%'$(CC) -c $(ingred)')

    @recipe('hello', ['hello.o'])          # @recipe(product, [ingredients])
    def file_hello(c):
        """create 'hello' command"""
        system(c%'$(CC) -o $(product) $(ingred)')

    @recipe
    def clean(c):
        rm_rf("**/*.o", "**/*~")

    ## or
    kookbook.load('@kook/books/clean.py')   # load 'clean' and 'sweep' recipes
    CLEAN.append("**/*.o")

See `User's Guide`_ for details.

.. _User's Guide: http://www.kuwata-lab.com/kook/pykook-users-guide.html

'''[1:]
    license          = 'MIT License'
    platforms        = 'any'
    download_url     = 'http://pypi.python.org/packages/source/K/%s/%s-%s.tar.gz' % (name, name, version)
    #download_url    = 'http://downloads.sourceforge.net/kook/%s-%s.tar.gz' % (name, version)
    #download_url    = 'http://downloads.sourceforge.net/kook/%s-%s.tar.gz' % (name, version)
    #download_url    = 'http://jaist.dl.sourceforge.net/sourceforge/kook/%s-%s.tar.gz' % (name, version)

    #py_modules       = ['kook']
    package_dir      = {'': 'lib'}
    scripts          = ['bin/pykook', 'bin/kk']
    packages         = ['kook']
    package_data     = {'kook': ['books/*.py']}
    #zip_safe        = False

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
    return locals()


setup(**_kwargs())
