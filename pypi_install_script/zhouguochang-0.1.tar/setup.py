# from setuptools import find_packages,setup
# setup(
#     name = 'zhouguochang',
#     version = '0.1',
#     packages = find_packages(),
# )
#

from distutils.core import setup
from setuptools import find_packages

setup(name='zhouguochang',  # 包名
      version='0.1',  # 版本号
      description='',
      long_description='周国昌学习第一次打包上传',
      author='',
      author_email='',
      url='',
      license='',
      install_requires=[],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Utilities'
      ],
      keywords='',
      packages=find_packages('src'),  # 必填，就是包的代码主目录
      package_dir={'': 'src'},  # 必填
      include_package_data=True,
      )
# !/usr/bin/env python




