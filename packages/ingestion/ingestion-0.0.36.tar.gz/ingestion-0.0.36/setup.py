#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os
from setuptools import setup, find_packages

#version = os.environ.get("package_version")
version = '0.0.36'

with open('README.md') as readme_file:
    readme = readme_file.read()


requirements = ['azure-keyvault-secrets==4.4.0',
'azure-storage-blob==12.12.0',
'pandas==1.4.2',
'openpyxl==3.0.9',
'xlrd==2.0.1',
'sqlalchemy==1.4.37',
'mysql-connector-python==8.0.13',
'adlfs==2022.4.0']


setup(
    author="Jefferson Farias",
    author_email='jefferson@fb.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9'
    ],
    description="Ingestão de dados",
    install_requires=requirements,
    long_description=readme,
    long_description_content_type='text/markdown',
    #include_package_data=True,
    keywords=[
        'ingestion',
    ],
    name='ingestion',
    #packages = find_packages(),  
    packages=['ingestion','ingestion.utils','ingestion.banco_dados','ingestion/banco_dados/ssl_ca_file'],
    package_data = {
        'ingestion': ['ingestion/banco_dados/ssl_ca_file/iotbd.crt.pem'],
    },
    include_package_data=True,
    version=version,
    python_requires='>=3.9'
)
