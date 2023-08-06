#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from setuptools import setup, find_packages

sys.path.insert(0, "src")
from scheduler import __version__

setup(
    name="sop-scheduler",
    version=__version__,
    description="SoPIoT Scheduler",
    author="caplab",
    author_email="caplab94@gmail.com",
    url="https://iris.snu.ac.kr",
    license="MIT",
    python_requires=">=3",
    install_requires=[],
    packages=find_packages("src"),
    package_dir={"": "src"},
)
