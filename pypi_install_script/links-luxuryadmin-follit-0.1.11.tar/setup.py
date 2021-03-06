from setuptools import setup, find_packages

NAME = 'links-luxuryadmin-follit'

setup(
    name=NAME,
    version="0.1.11",
    description='Luxury Admin for Django (follit fork)',
    long_description=open('README.md').read(),
    url='http://www.linkscreative.co.uk/',
    author='James Cleveland',
    author_email='jamescleveland@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    license="LICENSE.txt",
    package_data={
        '': ['*.txt', '*.rst']
    }
)
