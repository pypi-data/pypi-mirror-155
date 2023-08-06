#!/usr/bin/env python

# SPDX-FileCopyrightText: Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("requirements/base.txt") as f:
    requirements = f.read().splitlines()
    dependency_links = []
    for req in requirements:
        if req.startswith("git+"):
            requirements.remove(req)
            dependency_links.append(req)

with open("requirements/test.txt") as f:
    test_requirements = f.read().splitlines()

setup(
    author="Martijn van de Streek",
    author_email="martijn@mintlab.nl",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
    ],
    description="Storage infrastructure for the Minty framework",
    setup_requires=["pytest-runner"],
    install_requires=requirements,
    dependency_links=dependency_links,
    license="EUPL license",
    long_description_content_type="text/x-rst",
    long_description=readme,
    include_package_data=True,
    keywords="minty_infra_storage",
    name="minty_infra_storage",
    packages=find_packages(
        include=["minty_infra_storage", "minty_infra_storage.*"]
    ),
    package_data={"minty_infra_storage": ["py.typed"]},
    test_suite="tests",
    tests_require=test_requirements,
    url="https://gitlab.com/minty-python/minty-infra-storage",
    version="3.0.0",
    zip_safe=False,
)
