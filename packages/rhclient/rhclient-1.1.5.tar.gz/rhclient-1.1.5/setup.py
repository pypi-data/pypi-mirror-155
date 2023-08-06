#!/usr/bin/env python

# Setup file for rest harness
import setuptools
from setuptools import setup

setup(name='rhclient',
      version='1.1.5',
      description='Python REST Service Test utility',
      author='Robbie Reed',
      author_email='robbiereed@psg-inc.net',
      url='https://www.restharness.com',
      package_dir={"": "src"},
      packages=setuptools.find_packages(where="src"),
      python_requires=">=3.6",
      include_package_data=True,
      install_requires=['requests']
     )
