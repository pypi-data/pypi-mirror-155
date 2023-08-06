#!/usr/bin/env python

import setuptools
import os


def read(file_name: str) -> str:
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path) as f:
        return f.read()


setuptools.setup(
    name="pytest-circleci-parallelized-rjp",
    version="0.1.0",
    author="Ryan Wilson-Perkin",
    author_email="ryanwilsonperkin@gmail.com",
    maintainer="Rob Percival",
    maintainer_email="rob.percival87@gmail.com",
    license="MIT",
    url="https://github.com/RJPercival/pytest-circleci-parallelized",
    description="Parallelize pytest across CircleCI workers.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    py_modules=["pytest_circleci_parallelized"],
    python_requires=">=3.7",
    install_requires=["pytest"],
    classifiers=[
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["circleci-parallelized = pytest_circleci_parallelized"]},
)
