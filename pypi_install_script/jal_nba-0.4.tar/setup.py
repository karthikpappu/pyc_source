from setuptools import setup

setup(name='jal_nba',
      version='0.4',
      description='Retrieve info from NBA API at stats.nba.com/stats/',
      url='http://github.com/jalgraves/jal_nba',
      author='Jonny Graves',
      author_email='jal@jalgraves.com',
      license='MIT',
      packages=['jal_nba'],
      zip_safe=False,
      install_requires = [
          'pytz',
          'requests'
      ],
      include_package_data=True
      )
