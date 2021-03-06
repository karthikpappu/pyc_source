from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="djjunopass",
    version="1.1.4",
    author="Felix Cheruiyot",
    author_email="felix@junopass.com",
    description="JunoPass support for Django. Implement OTP and Passwordless strategy.",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/junopass/django-junopass",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'junopass-py==1.0.9',
    ]
)
