from setuptools import setup

setup(
  name = 'dekigokoro-py',
  #packages = ['dekigokoro-py'],
  version = '0.1',
  license='MIT',
  description = 'An asynchronous wrapper for the Dekigokoro API.',
  author = 'broman',
  author_email = 'ryan@broman.dev',
  url = 'https://github.com/broman/dekigokoro.py',
  download_url = 'https://github.com/broman/dekigokoro.py/archive/v0.1.tar.gz',
  install_requires= [
          'aiohttp',
          'asyncio',
      ],
  classifiers= [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)