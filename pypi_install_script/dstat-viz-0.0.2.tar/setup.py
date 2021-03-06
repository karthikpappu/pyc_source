from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dstat-viz',
    version='0.0.2',
    description='dstat visualizer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kuenishi/dstat-viz',
    author='@kuenishi',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='diagnosis',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.5, <4',

    install_requires=['matplotlib', 'pandas'],

    extras_require={
        'dev': ['check-manifest', 'pytest'],
        'test': ['coverage'],
    },

    entry_points={
        'console_scripts': [
            'dstat-viz=dstat_viz.main:main',
        ],
    },
    project_urls={
    },
)
