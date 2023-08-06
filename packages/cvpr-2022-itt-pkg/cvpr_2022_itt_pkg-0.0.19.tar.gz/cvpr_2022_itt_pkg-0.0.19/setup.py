import setuptools

VERSION = '0.0.19'

setuptools.setup(
    name="cvpr_2022_itt_pkg",
    version=VERSION,
    author="blank",
    package_dir={"core": "core", "ece": "ece", "prob": "prob", "physics": "physics"},
    #packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)