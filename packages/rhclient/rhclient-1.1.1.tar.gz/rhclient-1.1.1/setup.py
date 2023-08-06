#!/usr/bin/env python

# Setup file for rest harness

from setuptools import setup

setup(name='rhclient',
      version='1.1.1',
      description='Python REST Service Test utility',
      author='Robbie Reed',
      author_email='robbiereed@psg-inc.net',
      url='https://www.restharness.com',
      packages=['src'],
      python_requires=">=3.6",
      include_package_data=True,
      install_requires=['requests']
     )
