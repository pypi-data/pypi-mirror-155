from __future__ import absolute_import

from os import path

from setuptools import setup, find_packages

_dir = path.abspath(path.dirname(__file__))

with open(path.join(_dir, 'nc2gj', 'version.py')) as f:
  exec(f.read())

with open(path.join(_dir, 'README.md')) as f:
  long_description = f.read()

setup(name='nc2gj',
  version=__version__,
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://gitlab.mercator-ocean.fr/mirazoki/ecfas_geojason',
  author='Maialen Irazoki',
  author_email='mirazoki@mercator-ocean.fr',
  license='BSD Licence',

  packages=find_packages(include=["nc2gj"]),

  project_urls={
    'Repository': 'https://gitlab.mercator-ocean.fr/mirazoki/ecfas_geojason',
  },

  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'Environment :: Console',
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: BSD License',
  ],

  install_requires=[
     'xarray==2022.3.0',
     'netcdf4==1.5.8',
  ],

  setup_requires=['flake8'],
  python_requires='>=3.10'
)
