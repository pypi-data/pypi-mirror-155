from setuptools import setup, find_packages

VERSION = '0.0.5'

# Setting up
setup(
    name="cvpr_2022_itt_pkg",
    version=VERSION,
    author="blank",
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib'],
)