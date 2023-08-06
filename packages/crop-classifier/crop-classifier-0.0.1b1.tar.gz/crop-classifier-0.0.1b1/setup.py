#!/usr/bin/env python

from distutils.core import setup
from distutils.sysconfig import *

from pip._internal.req import parse_requirements
from setuptools import find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read().strip()

# install_reqs = parse_requirements('requirements.txt', session='hack')
# reqs = [str(ir.requirement) for ir in install_reqs]
try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

cmdclass = {}
ext_modules = []
py_inc = [get_python_inc()]

setup(name='crop-classifier',
      version='0.0.1b1',
      long_description = long_description,
      description='Unsupervised Crop Classification using Micro-spectral satellite imagery',
      long_description_content_type='text/markdown',
      author='Sumit Maan',
      author_email = 'sumitmaansingh@gmail.com',
      packages=find_packages(),
      url='https://github.com/sumit-maan/crop-classification',
      license='DEHAAT',
      cmdclass=cmdclass,
      ext_modules=ext_modules,
      setup_requires=['pytest-runner'],
      python_requires='>=3')
