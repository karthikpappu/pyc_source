from setuptools import setup, find_packages
import os

moduleDirectory = os.path.dirname(os.path.realpath(__file__))
exec(open(moduleDirectory + "/deckster/__version__.py").read())


def readme():
    with open(moduleDirectory + '/README.rst') as f:
        return f.read()


setup(name="deckster",
      version=__version__,
      description="CL tools to build a Reveal.js presentation from a single Multimarkdown file",
      long_description=readme(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Topic :: Utilities',
      ],
      keywords=['markdown, presentation'],
      url='https://github.com/thespacedoctor/deckster',
      download_url='https://github.com/thespacedoctor/deckster/archive/v%(__version__)s.zip' % locals(
      ),
      author='David Young',
      author_email='davidrobertyoung@gmail.com',
      license='MIT',
      packages=find_packages(),
      package_data={'deckster': [
          'resources/*/*', 'resources/*.*']},
      install_requires=[
          'pyyaml',
          'deckster',
          'frankenstein',
          'fundamentals'
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points={
          'console_scripts': ['deckster=deckster.cl_utils:main'],
      },
      zip_safe=False)
