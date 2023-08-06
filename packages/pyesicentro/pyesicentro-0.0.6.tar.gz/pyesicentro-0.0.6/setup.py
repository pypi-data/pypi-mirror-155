# setup.py
from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'Python 3 module to use with ESI Centro Thermostats'
LONG_DESCRIPTION = "A python module for accessing ESI Centro Thermostats.  This package was primarily created for use with HomeAssistant."

# Setting up
setup(
    name="pyesicentro",
    version=VERSION,
    author="John Matin McLaughlin",
    author_email="johnmartinmclaughlin@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=["pyesicentro"],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ]
)