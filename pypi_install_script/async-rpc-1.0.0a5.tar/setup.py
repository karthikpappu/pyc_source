
from setuptools import setup

with open('README.rst', 'rt') as f:
    long_description = f.read()

setup(
    name='async-rpc',
    version='1.0.0a5',
    author='Jan Seifert',
    author_email='jan.seifert@fotkyzcest.net',
    description='Non-blocking XML-RPC client for Python',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    license='BSD',
    url='https://github.com/seifert/async-rpc',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
    ],
    platforms=['any'],
    packages=['async_rpc'],
    zip_safe=True,
    install_requires=[
        'aiodns',
        'aiohttp',
        'async-timeout',
    ],
)
