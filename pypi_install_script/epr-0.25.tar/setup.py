from setuptools import setup

setup(
        name='epr',
        version='0.25',
        author='Luke Avery',
        author_email='cogmob@gmail.com',
        url='https://github.com/Cogmob/epr',
        description=('Tool for quickly adding debugging output'),
        packages=[
            'epr'
        ],
        install_requires=[
            'glob2'
        ],
        long_description=open('README.rst', 'r').read()
)
