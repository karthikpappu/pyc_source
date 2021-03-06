import re
import setuptools.command.test


class PyTest(setuptools.command.test.test):
    
    user_options = []
    
    def finalize_options(self):
        setuptools.command.test.test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        pytest.main(self.test_args)


extras_require = {
    'test': [
        'pytest >=2.5.2,<3',
        'pytest-cache >=1.0,<2',
        'pytest-cov >=1.7,<2',
        'pytest-pep8 >=1.0.6,<2',
    ],
}

setuptools.setup(
    name='janus-gateway',
    version=(
        re
        .compile(r".*__version__ = '(.*?)'", re.S)
        .match(open('janus.py').read())
        .group(1)
    ),
    url='https://github.com/mayfieldrobotics/janus-py/',
    author='Mayfield Robotics',
    author_email='dev+janus-py@mayfieldrobotics.com',
    license='BSD',
    description='Python client for Janus.',
    long_description=open('README.rst').read(),
    py_modules=['janus'],
    platforms='any',
    install_requires=[
        'blinker >=1.4,<2',
        'futures >=3.0.3,<4',
        'ws4py >=0.3.4,<0.4',
    ],
    tests_require=extras_require['test'],
    extras_require=extras_require,
    cmdclass={'test': PyTest},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
