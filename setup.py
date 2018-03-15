#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "CLAMServices",
    version = "1.5",
    author = "Maarten van Gompel",
    author_email = "proycon@anaproy.nl",
    description = ("A collection of CLAM Webservices for various of our NLP tools"),
    license = "GPL",
    keywords = "clam webservice rest nlp computational_linguistics rest",
    url = "https://proycon.github.io/clam",
    packages=['clamservices','clamservices.wsgi','clamservices.config','clamservices.wrappers'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3", #3.0, 3.1 and 3.2 are not supported by flask
        "Programming Language :: Python :: 3.4", #3.0, 3.1 and 3.2 are not supported by flask
        "Programming Language :: Python :: 3.5", #3.0, 3.1 and 3.2 are not supported by flask
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    package_data = {'clamservices':['wrappers/*.sh','wsgi/*.wsgi','config/*.yml'] },
    include_package_data=True,
    install_requires=['CLAM >= 2.3']
)
