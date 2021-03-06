from setuptools import setup, find_packages

try:
    with open('README.rst') as file:
        long_description = file.read()
except Exception as error:
    print("Could not find README.rst for long description. Error: {}".format(
        error))
    print("Leaving long_description as None")
    long_description = None

setup(
    name='mathpixy',
    author='elias julian marko garcia',
    author_email='elias.jm.garcia@gmail.com',
    description='gui for mathpix',
    url='https://github.com/ejmg/mathpixy',
    version='0.0.1dev',
    packages=find_packages(),
    entry_points={
        "console_scripts": ['mathpixy = mathpixy.mathpixy:cli'],
    },
    install_requires=[],
    license='MIT',
    long_description=long_description)
