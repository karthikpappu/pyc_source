#from distutils.core import setup
from setuptools import setup, find_packages

VERSION = '0.1.9'
PROJECT_NAME = 'py-social'

tests_require = [
    'nose',
    'coverage',
]

install_requires = [
    'six',
    'requests',
    'python-dateutil',
    'simplejson',
    'tweepy',
    'facebook-sdk',
    'selenium',
]

setup(name='%s' % PROJECT_NAME,
      url='https://github.com/paulocheque/%s' % PROJECT_NAME,
      author="paulocheque",
      author_email='paulocheque@gmail.com',
      keywords='',
      description='',
      license='MIT',
      classifiers=[
          # 'Framework :: Tornado',
          'Operating System :: OS Independent',
          'Topic :: Software Development'
      ],

      version='%s' % VERSION,
      install_requires=install_requires,
      tests_require=tests_require,
      # test_suite='runtests.runtests',
      # extras_require={'test': tests_require},

      packages=find_packages(),
)

