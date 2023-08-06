#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from meta import __version__

from setuptools import setup, find_packages

install_requirements = [
    'python-dotenv',
    'dataclasses',
    'pymysql',
    'contracts-lib-py==0.11.0',
    'boto3',
    'botocore',
    'requests',
    'nevermined-sdk-py==0.12.0',
    'nevermined-metadata-driver-filecoin==0.3.0',
    'web3',
    'retry',
    'pytest',
    'pytest-mock',
    'awswrangler'
]

# Required to run setup.py:
setup_requirements = ['pytest-runner', ]

test_requirements = [
    'pytest',
]


setup(
    author="nevermined-io",
    author_email='root@nevermined.io',
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    description="🐳 Nevermined Python SDK.",
    extras_require={
        'test': test_requirements
    },
    install_requires=install_requirements,
    license="Apache Software License 2.0",
    long_description='',
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='defi_common_lib',
    name='defi_common_lib',
    setup_requires=setup_requirements,
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    test_suite='tests',
    tests_require=test_requirements,
    version=__version__,
    zip_safe=False,
)
