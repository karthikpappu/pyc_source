from distutils.core import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
  name = 'asyhttp',
  packages = ['asyhttp'],
  version = '0.2',
  description = 'Simple module to perform asynchronous HTTP requests using asyncio and aiohttp',
  long_description=long_description,
  author = 'ax',
  author_email = 'ax.tryin@gmail.com',
  url = 'https://github.com/ax/asyhttp',
  download_url = 'https://github.com/ax/asyhttp/archive/0.2.tar.gz',
  keywords = ['aiohttp','asyncio','http','async','asynchronous','http-requests']
)
