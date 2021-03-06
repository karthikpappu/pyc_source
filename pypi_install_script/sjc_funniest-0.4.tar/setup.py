from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='sjc_funniest',
      version='0.4',
      description='The funniest joke in the world',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['sjc_funniest'],
      install_requires=[
          'markdown',
      ],
      entry_points = {
        'console_scripts': ['funniest-joke=funniest.command_line:main'],
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
