#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup

settings = dict()

root_path = os.path.dirname(os.path.realpath(__file__))

with open("{0}/kong_hmac/__version__.py".format(root_path), "rb") as version:
    setup_info = version.read()
    exec(setup_info)

with open("{0}/README.rst".format(root_path), "rb") as file_readme:
    readme = file_readme.read().decode("utf-8")

settings.update(name=__package_name__,
                version=__version__,
                description=__title__,
                long_description=readme,
                author=__author__,
                author_email=__author_email__,
                license=__license__,
                url=__url__,
                packages=find_packages(),
                zip_safe=False,
                classifiers=__classifiers__)

setup(**settings)
