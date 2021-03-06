import setuptools

with open('README.md', "r") as readme:
    long_description = readme.read()

with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

setuptools.setup(
  name='PygameMenus',
  version='0.0.6',
  license='MIT',
  description='Make menus with pygame',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author='Pedro Azevedo',
  author_email='p.costa.azevedo@gmail.com',
  url='https://github.com/MrComboF10/PygameMenus',
  install_requires=required,
  packages=setuptools.find_packages(),
  classifiers=[
    'Development Status :: 4 - Beta',
    'Operating System :: OS Independent',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: pygame',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)