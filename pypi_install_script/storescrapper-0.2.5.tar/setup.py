from setuptools import setup

# We add the path to the tests so that the celeryconfig.py file may be found
import sys
sys.path.append('storescrapper/tests')

setup(
    name='storescrapper',
    version='0.2.5',
    author='Vijay Khemlani',
    author_email='vkhemlan@gmail.com',
    packages=[
        'storescrapper',
        'storescrapper.stores',
        'storescrapper.exceptions',
        'storescrapper.tests',
        'storescrapper.tests.scrappers'
    ],
    scripts=[],
    url='https://github.com/SoloTodo/storescrapper',
    license='LICENSE.txt',
    description='Web scrapping API for selected stores',
    long_description=open('README.rst').read(),
    tests_require=[
        'nose>=1.1.2'
    ],
    test_suite='nose.collector',
    install_requires=[
        'mechanize==0.2.5',
        'BeautifulSoup==3.2.1',
        'celery==2.5.5',
    ],
)
