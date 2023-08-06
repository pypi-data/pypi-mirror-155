import setuptools

VERSION = '0.0.20'

setuptools.setup(
    name="cvpr_2022_itt_pkg",
    version=VERSION,
    author="blank",
    packages=['cvpr_2022_itt_pkg', 'cvpr_2022_itt_pkg/core',
              'cvpr_2022_itt_pkg/ece', 'cvpr_2022_itt_pkg/prob', 'cvpr_2022_itt_pkg/physics'],
    python_requires=">=3.6",
)