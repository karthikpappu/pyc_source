"""
wutils provides a collection of useful functions/classes for data analysis and ML.
"""
from setuptools import setup

setup(
    name='wutils',
    version='0.1.0',
    author='William Shioa',
    author_email='willshiao@gmail.com',
    packages=['wutils', 'wutils.test'],
    scripts=[],
    url='http://pypi.python.org/pypi/wutils/',
    license='LICENSE',
    description='A collection of useful functions/classes for data analysis and ML.',
    long_description=open('README.md').read(),
    install_requires=[
        "scikit-learn",
        "numpy",
        "seaborn",
        "pytest",
    ],
)
