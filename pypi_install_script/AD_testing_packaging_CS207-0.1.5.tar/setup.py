import setuptools 

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setuptools.setup(
    name='AD_testing_packaging_CS207',
    version='0.1.5',
    author='Shenghao Jiang, Isabelle Feldhaus, Robbert Struyven, William Wang',
    author_email=" ",
    description='Automatic Differentiation Package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    keywords=['Automatic differentiation', 'gradients', 'Python'],
    url='https://github.com/cs207-f18-WIRS/cs207-FinalProject',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
