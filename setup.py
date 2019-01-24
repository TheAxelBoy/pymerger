#!/usr/bin/env python
# Copyright (c) Alex-Christian Lazau
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from setuptools import setup, find_packages
import codecs

import pymerger

with codecs.open('README.rst', 'r', 'utf-8') as fd:
    long_description = fd.read()

setup(
    name="PyMerger",
    version=pymerger.__version__,
    url="https://github.com/TheAxelBoy/pymerger",
    author="Alex-Christian Lazau",
    author_email="alex.lazau@gmail.com",
    maintainer="Alex-Christian Lazau",
    maintainer_email="alex.lazau@gmail.com",
    description='A file merger for Python code.',
    long_description=long_description,
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "yapf"
    ],
    classifiers=[
        "Environment :: Console",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries"
    ],
    entry_points={
        'console_scripts': ['pymerger = pymerger:run_pymerger'],
    }
)
