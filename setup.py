from setuptools import setup
from setuptools import find_packages
import re
from os.path import abspath, dirname, join

CURDIR = dirname(abspath(__file__))

with open("README.rst", "r", encoding='utf-8') as fh:
    long_description = fh.read()

with open(join(CURDIR, 'src', 'DataDriver', 'DataDriver.py'), encoding='utf-8') as f:
    VERSION = re.search("\n__version__ = '(.*)'", f.read()).group(1)

setup(
    name="robotframework-datadriver",
    version=VERSION,
    author="René Rohner(Snooz82)",
    author_email="snooz@posteo.de",
    description="A library for Data-Driven Testing.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Snooz82/robotframework-datadriver",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Framework :: Robot Framework",
    ],
    install_requires=[
        'robotframework >= 3.1',
        'docutils',
        'Pygments'
    ],
    extras_require={
            'xls':  [
                'numpy',
                'pandas',
                'xlrd >= 1.0.0'
            ]
    },
    python_requires='>=3.6'
)
