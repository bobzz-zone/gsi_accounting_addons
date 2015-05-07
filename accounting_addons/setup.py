# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='accounting_addons',
    version=version,
    description='App for additional accounting module',
    author='Myme',
    author_email='myme.technology@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
