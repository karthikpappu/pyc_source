from setuptools import setup

setup(
    name = 'pysster',
    version = '1.2.2',
    description = 'a Sequence/STructure classifiER for biological sequences',
    url = 'https://github.com/budach/pysster',
    author = 'Stefan Budach',
    author_email = 'budach@molgen.mpg.de',
    license = 'MIT',
    install_requires =  [
        'numpy>=1.14.0',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'keras<2.3.0',
        'tensorflow<2.0',
        'h5py',
        'logging_exceptions',
        'Pillow',
        'forgi',
        'fastcluster'
    ],
    packages = ['pysster'],
    python_requires = '>=3.5',
    include_package_data = True,
    zip_safe = False
)
