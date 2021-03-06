from setuptools import setup
from setuptools import find_packages

LONG_DESCRIPTION = "\n\n".join([
    open('README.md').read(),
])

setup(
    name='prog_lang_detector',
    version='0.2.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    url='https://github.com/Bystroushaak/prog_lang_detector',
    license='MIT',
    author='Bystroushaak',
    author_email='bystrousak@kitakitsune.org',
    description='Detect programming language using Markov chains.',

    classifiers=[
        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python",
        "Programming Language :: Python :: 3",

        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        'console_scripts': [
            'prog_lang_detector=prog_lang_detector.classify:main',
            'prog_lang_generate_models=prog_lang_detector.generate_models:main',
        ],
    }
)
