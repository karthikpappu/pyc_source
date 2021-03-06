from setuptools import setup, find_packages
setup (
  name = 'tessfpe',
  packages = find_packages(),
  package_data = {
      'tessfpe': [
                  'data/files/*.tsv',   # Add all of the TSV files in the package
                  'data/files/*.fpe',   # Add all of the preconfigured FPE programs in the package
                  'dhu/MemFiles/*.bin'  # Add all of the binary files to be uploaded to the FPE
                 ],
  },
  version = '6.1.12.dev9',
  description = 'Software to accompany the Focal Plane Electronics (FPE) for the Transiting Exoplanet Survey Satellite (TESS)',
  author = 'John Doty',
  author_email = 'jpd@noqsi.com',
  url = 'https://github.com/TESScience/FPE', # use the URL to the github repo
  download_url = 'https://github.com/TESScience/FPE/tarball/6.1.12.dev9',
  install_requires=[
      'grako>=3.6.3',
      'sh>=1.11',
  ],
)
