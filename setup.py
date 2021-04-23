import os
from setuptools import setup

required = []

# We are installing the gmpy2 module to build the docs, but the C libraries
# required to build snappy aren't available on RTD, so we need to exclude it
# from the installed dependencies here, and mock it for import in docs/source/conf.py
# using the autodoc_mock_imports parameter:
if not os.getenv("READTHEDOCS"):
    required.append("gmpy2")

setup(install_requires=required)
