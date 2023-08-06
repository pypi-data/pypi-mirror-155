#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wd_pytools",
    version="0.0.3",
    author="teshin",
    author_email="1443965173@qq.com",
    description="This is the tools for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://pypi.org",
    install_requires=[],
    packages=setuptools.find_packages(exclude=("test")),
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        # "Programming Language :: Python :: 2",
        # "Programming Language :: Python :: 2.6",
        # "Programming Language :: Python :: 2.7",
        # "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.3",
        # "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.10"
    ),
    # exclude_package_data={'': ["example-pkg/test.py", "example-pkg/config.txt"]},
)
