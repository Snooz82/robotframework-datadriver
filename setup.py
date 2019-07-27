# coding=utf-8
import io

from setuptools import setup
from setuptools import find_packages
import re
from os.path import abspath, dirname, join

CURDIR = dirname(abspath(__file__))

with io.open("README.rst", "r", encoding='utf-8') as fh:
    long_description = fh.read()

with io.open(join(CURDIR, 'src', 'DataDriver', 'DataDriver.py'), encoding='utf-8') as f:
    VERSION = re.search("\n__version__ = '(.*)'", f.read()).group(1)

setup(
    name="robotframework-datadriver",
    version=VERSION,
    author="René Rohner(Snooz82)",
    author_email="snooz@posteo.de",
    description="A library for Data-Driven Testing. (Oldies Version 2.7 compatibility release)",
    long_description=long_description,
    url="https://github.com/Snooz82/robotframework-datadriver",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Framework :: Robot Framework",
    ],
    install_requires=[
        'numpy',
        'pandas',
        'xlrd',
        'robotframework >= 3.1'],
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*'
)
