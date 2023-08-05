#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    include_package_data=True,
    name='simple-plugin-manager',
    version='0.0',
    author='Florian Scherf',
    url='https://github.com/fscherf/simple-plugin-manager',
    author_email='mail@florianscherf.de',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    scripts=[],
    entry_points={},
)
