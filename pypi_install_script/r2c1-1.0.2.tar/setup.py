from setuptools import setup

setup(
    name='r2c1',
    version='1.0.2',
    packages=['r2c1'],
    url='https://github.com/chinapnr/r2c1',
    license='MIT',
    author='david.yi',
    author_email='wingfish@gmail.com',
    description='Convert string like command with args and options to json',

    install_requires=[
        'fish_base'
    ],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],

    include_package_data=True

)
