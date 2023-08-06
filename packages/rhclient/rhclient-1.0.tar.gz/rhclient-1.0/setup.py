#!/usr/bin/env python

# Setup file for rest harness

from setuptools import setup

setup(name='rhclient',
      version='1.0',
      description='Python REST Service Test utility',
      author='Robbie Reed',
      author_email='robbiereed@psg-inc.net',
      url='https://www.restharness.com',
      packages=['src'],
      install_requires=['requests']
     )
