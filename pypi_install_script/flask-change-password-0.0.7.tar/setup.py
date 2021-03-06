# Copyright 2019 Andrew Rowe.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from codecs import open

from setuptools import setup

long_description = open('README.rst', 'r', encoding='utf-8').read()

setup(
    name='flask-change-password',

    version='0.0.7',

    description='password change and set pages for Flask.',
    long_description=open('README.rst', 'r', encoding='utf-8').read(),
    long_description_content_type='text/x-rst',

    url='https://github.com/Martlark/flask-change-password',
    download_url='https://github.com/Martlark/flask-change-password/archive/0.0.7.tar.gz',

    author='Andrew Rowe',
    author_email='rowe.andrew.d@gmail.com',

    license='Apache Software License',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
    ],
    keywords='flask change password page',

    packages=['flask_change_password'],
    include_package_data=True,
    install_requires=['flask>=0.11', 'flask-wtf', 'WTForms', 'requests'],
)
