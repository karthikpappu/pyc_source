from distutils.core import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name='sarus',         # How you named your package folder (MyLib)
  packages=['sarus'],
  version='0.1.17',
  license='Apache License 2.0',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='Python client for the Sarus Gateway.',
  long_description=long_description,
  author='Sarus Technologies',                   # Type in your name
  author_email='contact@sarus.tech',      # Type in your E-Mail
  url='https://sarus.tech',
  #  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords=['differential privacy', 'AI', 'Data privacy'],   # Keywords that define your package best
  install_requires=[
          'cloudpickle >=1.2',
          'tensorflow >=2.0',
          'numpy >=1.17',
          'pandas >=1.0.3',
          'matplotlib >=3.1',
          'tensorflow-io >=0.11'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
