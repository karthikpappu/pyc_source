from setuptools import setup
import os
import fnmatch
import sys
import imp
import subprocess


def find_package_data_files(directory):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, '*'):
                filename = os.path.join(root, basename)
                yield filename.replace('cfplot/', '', 1)


package_data = [f for f in find_package_data_files('cfplot/colourmaps')]


setup(
    name = "cf-plot",
    version = "3.0.6",
    author = "Andy Heaps",
    author_email = "andy.heaps@ncas.ac.uk",
    packages = ['cfplot'],
    package_dir = {'cfplot':'cfplot'},
    package_data = {'cfplot': package_data},
    include_package_data = True,
    install_requires = ['matplotlib >=3.1.0'],
    url = "http://ajheaps.github.io/cf-plot",
    license = 'LICENSE.txt',
    description = "Climate contour, vector and line plots in Python",
    long_description = open('README.txt').read(),
    long_description_content_type = "text/markdown"
)



