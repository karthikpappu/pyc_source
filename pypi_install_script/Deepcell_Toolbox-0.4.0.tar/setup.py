# Copyright 2016-2019 The Van Valen Lab at the California Institute of
# Technology (Caltech), with support from the Paul Allen Family Foundation,
# Google, & National Institutes of Health (NIH) under Grant U24CA224309-01.
# All rights reserved.
#
# Licensed under a modified Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.github.com/vanvalenlab/deepcell-toolbox/LICENSE
#
# The Work provided may be used for non-commercial academic purposes only.
# For any other use of the Work, including commercial use, please contact:
# vanvalenlab@gmail.com
#
# Neither the name of Caltech nor the names of its contributors may be used
# to endorse or promote products derived from this software without specific
# prior written permission.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
from setuptools import setup
from setuptools import find_packages

VERSION = '0.4.0'

setup(name='Deepcell_Toolbox',
      version=VERSION,
      description='The pre- and post-processing functions module for '
                  'deepcell-tf.',
      author='Van Valen Lab',
      author_email='vanvalenlab@gmail.com',
      url='https://github.com/vanvalenlab/deepcell-toolbox',
      download_url='https://github.com/vanvalenlab/'
                   'deepcell-toolbox/tarball/{}'.format(VERSION),
      license='LICENSE',
      install_requires=['keras-retinanet',
                        'numpy',
                        'scipy',
                        'scikit-image'],
      extras_require={
          'tests': ['pytest',
                    'pytest-pep8',
                    'pytest-cov']},
      packages=find_packages())
