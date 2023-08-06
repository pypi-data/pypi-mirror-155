# coding: utf-8

"""
    Portfolio Personal Inversiones API
"""


from setuptools import setup, find_packages

NAME = "ppi_client"
VERSION = "1.1.3"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    # "setuptools >= 52.0.0",
    "requests >= 2.25.1",
    "setuptools >= 52.0.0",
    "requests >= 2.25.1",
    "vcrpy >= 1.10.3",
    "pytest >= 3.0.3",
    "flake8 >= 3.8.4",
    "requests-toolbelt >= 0.9.1",
    "signalrcoreppi >= 0.9.2"
]


setup(
    name=NAME,
    version=VERSION,
    author="PPI SDK <api@portfoliopersonal.com>",
    author_email="api@portfoliopersonal.com",
    keywords=["SDK", "Portfolio Personal Inversiones API"],
    description="Portfolio Personal Inversiones API",
    long_description=open("README.md", encoding="utf8").read(),
    packages=find_packages(),
    url="",
    install_requires=REQUIRES
)
