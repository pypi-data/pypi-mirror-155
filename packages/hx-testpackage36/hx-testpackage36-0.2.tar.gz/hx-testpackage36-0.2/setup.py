#!/usr/bin/env python
# coding: utf-8


from setuptools import setup, find_packages
setup(
    name='hx-testpackage36',
    version='0.2',
    author='Tector Pro',
    description='Testing the efficientcy of Inspector',
    packages=find_packages(),
    python_requires=">3.0",
    install_requires=["hx-testpackage27"]
)
