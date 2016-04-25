#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from setuptools import setup

sys.path.append('./src')

information = dict(
    name='whiteplanes',
    version='0.0.1',
    description='Whitespace interpreter written in Python',
    author='Takuya Katsurada',
    author_email='mail@nutcrack.io',
    packages=['whiteplanes'],
    package_dir={'whiteplanes':'./src'},
    license='MIT License',
    test_suite='test',
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License'
    ],
)
setup(**information)