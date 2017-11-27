import os
from setuptools import setup, find_packages


# Utility function to read a file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="hmPy",
    version="0.1.0",
    description="A python library for generating human machine interfaces",
    long_description=read("README.rst"),
    url="https://github.com/PyLC/hmPy",
    license="GPL v3",
    packages=find_packages(exclude=["test"]),
    install_requires=[
        'PyQt5===5.9',
        'PyQtChart===5.9'
    ]
)
