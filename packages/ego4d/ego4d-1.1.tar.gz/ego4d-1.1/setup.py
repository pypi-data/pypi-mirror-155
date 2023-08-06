#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates. All Rights Reserved.

from setuptools import find_packages, setup

setup(
    name="ego4d",
    version="1.1",
    author="FAIR",
    author_email='info@ego4d-data.org',
    url="https://github.com/facebookresearch/Ego4d",
    install_requires=[
        "boto3",
        "tqdm",
        # "av",
        # "torch",
        # "torchvision",
        # "pytorch_lightning",
        # "matplotlib",
        # "simplejson",
        # "matplotlib",
        # "pandas",
    ],
    tests_require=[
        "pytest",
        "moto",
    ],
    packages=find_packages("ego4d/cli", exclude=["features", "tests"]),
    entry_points={
        'console_scripts': ['ego4d=ego4d.cli.cli:main'],
    }
)
