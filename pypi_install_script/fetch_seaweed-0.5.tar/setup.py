from setuptools import setup

setup(
        name='fetch_seaweed',
        version='0.5',
        scripts=['fetch_seaweed.py', '__init__.py'],
        install_requires=[
            'opencv-python',
            'numpy',
            'requests'
            ]
    )
