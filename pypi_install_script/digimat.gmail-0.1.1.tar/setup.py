from setuptools import setup, find_packages

setup(
    name='digimat.gmail',
    version='0.1.1',
    description='Digimat Google Mail sender',
    namespace_packages=['digimat'],
    author='Frederic Hess',
    author_email='fhess@splust.ch',
    url='http://www.digimat.ch',
    license='PSF',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'Pillow',
        'setuptools'
    ],
    dependency_links=[
        ''
    ],
    zip_safe=False)
