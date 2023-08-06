# coding: utf-8
import os
import re

from setuptools import setup, find_packages

module_file = open("refinitiv/data/__init__.py").read()
metadata = dict(re.findall(r'__([a-z]+)__\s*=\s*"([^"]+)"', module_file))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="refinitiv-data",
    version=metadata["version"],
    description="Python package for retrieving data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://developers.refinitiv.com/en/api-catalog/refinitiv-data-platform/refinitiv-data-library-for-python",
    author="REFINITIV",
    author_email="",
    license="Apache 2.0",
    data_files=[("", ["LICENSE.md", "CHANGES.txt"])],
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "tests_*"]
    ),
    package_data={"": [os.path.join("refinitiv-data.config.json")]},
    zip_safe=False,
    python_requires=">3.6",
    install_requires=[
        "appdirs>=1.4.3",
        "eventemitter>=0.2.0",
        "pyee",
        "httpx>=0.18,<=0.22.0",
        "httpcore<=0.14.5",
        "mysql-connector-python",
        "numpy>=1.11.0",
        "pandas>=1.3.5,<1.4.0",
        "python-configuration>=0.8.2",
        "python-dateutil",
        "requests",
        "scipy",
        "six",
        "tenacity>=8.0,<8.1",
        "watchdog>=0.10.2",
        "websocket-client>=0.58.0,!=1.2.2",
        "pyhumps~=3.0.2",
    ],
)
