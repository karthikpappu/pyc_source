# Custom error (in case user does not have setuptools)
class DependencyError(Exception): pass

# Try to import setuptools (if it fails, the user needs that package)
try: 
    from setuptools import setup, find_packages
except:
    raise(DependencyError("Missing python package 'setuptools'.\n  pip install --user setuptools"))

import os
# Go to the "about" directory in the package directory
PACKAGE_NAME = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)),PACKAGE_NAME,"about")
# Convenience function for reading information files
def read(f_name, dir_name=DEFAULT_DIRECTORY, processed=True):
    text = []
    with open(os.path.join(dir_name, f_name)) as f:
        if processed:
            for line in f:
                line = line.strip()
                if (len(line) > 0) and (line[0] != "%"):
                    text.append(line)
        else:
            text = f.read()
    return text

if __name__ == "__main__":
    #      Read in the package description files     
    # ===============================================
    package = PACKAGE_NAME
    version =read("version.txt")[0]
    description = read("description.txt")[0]
    requirements = read("requirements.txt")
    keywords = read("keywords.txt")
    classifiers = read("classifiers.txt")
    name, email, git_username = read("author.txt")

    setup(
        author = name,
        author_email = email,
        name=package,
        packages=find_packages(exclude=[]),
        include_package_data=True,
        install_requires=requirements,
        version=version,
        url = 'https://github.com/{git_username}/{package}'.format(
            git_username=git_username, package=package),
        download_url = 'https://github.com/{git_username}/{package}/archive/{version}.tar.gz'.format(
            git_username=git_username, package=package, version=version),
        description = description,
        keywords = keywords,
        python_requires = '>=2.7',
        license='MIT',
        classifiers=classifiers
    )
