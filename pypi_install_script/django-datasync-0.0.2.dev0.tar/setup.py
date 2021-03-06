from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='django-datasync',
      version='0.0.2',
      description=u"Sync environment",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Geert Dekkers",
      author_email='geert@djangowebstudio.com',
      url='https://bitbucket.org/geert2705/django-datasync',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'Django',
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      datasync=datasync.scripts.cli:cli
      """
      )
