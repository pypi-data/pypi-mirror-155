#!/usr/bin/env python3

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='xtesting-db-populate',
    version="1.3.0",
    description='xtesting db populate script',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://gitlab.com/Orange-OpenSource/lfn/tools/xtesting-db-populate',
    author='Orange OpenSource',
    license='Apache 2.0',
    packages=find_packages('.'),
    py_modules=[splitext(basename(path))[0] for path in glob('*.py')],
    include_package_data=True,
    scripts=["xtesting-db-populate"],
    install_requires=[
        "pyyaml",
        "requests"
    ],
    setup_requires=["pytest-runner"],
    tests_require=[
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "mock",
        "requests_mock"
    ],
    zip_safe=False)
