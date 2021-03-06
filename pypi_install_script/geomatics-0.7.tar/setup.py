from setuptools import setup

version = '0.7'

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name='geomatics',
    packages=['geomatics'],
    version=version,
    description='Geospatial tools in pure python developed by Riley Hales as part of a Master\'s Thesis '
                'at Brigham Young University',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Riley Hales',
    project_urls=dict(Documentation='https://geomatics.readthedocs.io',
                      Source='https://github.com/rileyhales/geomatics'),
    license='BSD 3-Clause',
    python_requires='>=3',
    install_requires=['rasterio', 'rasterstats', 'pygrib', 'netcdf4', 'python-dateutil', 'numpy', 'pandas', 'requests']
)
