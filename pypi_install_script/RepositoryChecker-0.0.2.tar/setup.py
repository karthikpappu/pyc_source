import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='RepositoryChecker',
    version='0.0.2',
    author="Théo \"Nydareld\" Guerin",
    author_email="theo.guerin.pro@gmail.com",
    description="Check repository and corect it with parametred actions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nydareld/RepositoryChecker",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
