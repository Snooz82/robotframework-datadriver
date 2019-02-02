import setuptools
import re
from os.path import abspath, dirname, join

CURDIR = dirname(abspath(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(join(CURDIR, 'src', 'DataDriver', 'DataDriver.py')) as f:
    VERSION = re.search("\n__version__ = '(.*)'", f.read()).group(1)

setuptools.setup(
    name="robotframework-datadriver",
    version=VERSION,
    author="René Rohner(Snooz82)",
    author_email="snooz@posteo.de",
    description="A library for data driven tests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Snooz82/robotframework-datadriver",
    package_dir={'':'src'},
    packages=setuptools.find_packages('src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Framework :: Robot Framework",
    ],
)
