from __future__ import print_function
from setuptools import setup

setup(
  name='ansibull',
  packages=['ansibull'],
  version='0.1',
  description=("You meant to type ansible. You ended up here. I don't want "
               "anybody being able to use this to hack you. So I made this."),
  author='Joshua "jag" Ginsberg',
  author_email='jag@flowtheory.net',
  url='https://github.com/j00bar/ansibull',
  install_requires=['ansible']
)

print('*** WARNING ***')
print('You mistyped "ansible" and instead typed "ansibull". I have ')
print('installed Ansible anyway, but you really should uninstall ansibull ')
print('and make sure your dependencies are not misspelled.')
print('*** CARRY ON ***')
