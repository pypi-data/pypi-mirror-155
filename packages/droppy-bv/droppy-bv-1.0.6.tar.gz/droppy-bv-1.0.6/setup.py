#!/usr/bin/env python
import sys
from setuptools import setup
from droppy import __version__

package_dir= { "droppy" : 'droppy' ,
               "droppy.Reader" : r"./droppy/Reader" ,
               "droppy.pyplotTools" : r"./droppy/pyplotTools" ,
               "droppy.TimeDomain" : r"./droppy/TimeDomain" ,
               "droppy.numerics" : r"./droppy/numerics" ,
               "droppy.Form" : r"./droppy/Form" ,
               "droppy.interpolate" : r"./droppy/interpolate" ,
             }

packages = package_dir.keys()

long_description = open('README.md', 'r').read()

with open('requirements.txt') as f:
  required = f.read().splitlines()

setup(name='droppy-bv',
      version=__version__,
      description='Research Department BV M&O open library, related to waves and sea-keeping',
      long_description=long_description,
      author='Research Department BV M&O',
      author_email='',
      url= r'https://github.com/BV-DR/droppy',
      packages = packages ,
      package_dir = package_dir ,
      install_requires = required ,
      classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
     )
