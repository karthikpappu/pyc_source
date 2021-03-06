from setuptools import setup, find_packages
import driver

setup(
  name = 'phantooom-qingcloud-cli',
  version = 0.3,
  packages = find_packages(),
  install_requires = ['requests','PyYAML>=3.1'],
  entry_points = {
    'console_scripts': [
      'homework-qingcluod-cli = driver:main']
  },

  author = 'phantooom',
  author_email = 'zouruixp@sina.com',
  description = 'homework-qingcluod-cli',
  license = 'MIT',
  keywords = 'homework',
  url = 'http://fullstack.love',
  scripts=['bin/qingcloud'],
)