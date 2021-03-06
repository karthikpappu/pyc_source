from setuptools import setup, find_packages

setup(
    name='lupin_utils',
    version='0.2.10',
    author='Henry',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'Cython==0.29.11',
        'numpy==1.16.4',
        'scikit-learn==0.21.2',
        'pandas==0.24.2',
        'mlflow==0.8.2',
        'xgboost==0.82',
        'odps==3.5.1',
        'pymysql==0.9.3',
        'pymongo==3.7.2',
        'pyyaml==5.1.1',
        'scipy==1.1.0',
        'implicit==0.3.8',
        'gensim==3.8.0',
        'oss2==2.6.1',
        'matplotlib==3.1.1',
        'psutil==5.6.3',
        'pyhdfs== 0.2.2'
    ]

)
