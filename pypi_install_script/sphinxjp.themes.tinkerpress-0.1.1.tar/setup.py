# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os, sys

version = '0.1.1'
long_description = '\n'.join([
        open(os.path.join("src", "README.txt")).read(),
        open(os.path.join("src", "AUTHORS.txt")).read(),
        open(os.path.join("src", "HISTORY.txt")).read(),
        ])

classifiers = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Topic :: Software Development",
    "Topic :: Software Development :: Documentation",
    "Topic :: Text Processing :: Markup",
]

setup(
    name='sphinxjp.themes.tinkerpress',
    version=version,
    description='A tinkerer theme like some famous blogging tool.',
    long_description=long_description,
    classifiers=classifiers,
    keywords=['tinkerer', 'sphinxjp', 'reStructuredText', 'theme'],
    author='Shoji KUMAGAI',
    author_email='take dot this dot 2 dot your dot grave at gmail dot com',
    url='https://github.com/shkumagai/sphinxjp.themes.tinkerpress',
    license='MIT',
    namespace_packages=['sphinxjp', 'sphinxjp.themes'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'': ['buildout.cfg']},
    include_package_data=True,
    install_requires=[
        'setuptools',
        'docutils',
        'tinkerer',
        'sphinxjp.themecore',
        'pygments-style-solarized',
    ],
    entry_points="""
        [sphinx_themes]
        path = sphinxjp.themes.tinkerpress:template_path

    """,
    zip_safe=False,
)
