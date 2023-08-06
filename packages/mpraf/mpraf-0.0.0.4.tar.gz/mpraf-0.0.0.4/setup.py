from setuptools import find_packages, setup

# Package meta-data.
NAME = 'mpraf'
DESCRIPTION = 'MPRAF-Multi-layer Puzzle Recommendation Algorithm Frame'
URL = 'http://zhihengyang.com'
EMAIL = 'zach-young@outlook.com'
AUTHOR = 'Zhiheng Yang 杨志恒'
REQUIRES_PYTHON = '>=3.9.0'
VERSION = '0.0.0.4'
packages=['mpraf', "mpraf.algs", "mpraf.utility"],

# What packages are required for this module to be executed?
REQUIRED = []

# Setting.
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    license="MIT"
)