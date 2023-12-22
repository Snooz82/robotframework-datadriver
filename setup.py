import re
from pathlib import Path

from setuptools import find_packages, setup

with Path("Readme.rst").open(encoding="utf-8") as fh:
    long_description = fh.read()

with (Path(__file__).resolve().parent / "src" / "DataDriver" / "DataDriver.py").open(
    encoding="utf-8"
) as f:
    VERSION = re.search('\n__version__ = "(.*)"', f.read()).group(1)

setup(
    name="robotframework-datadriver",
    version=VERSION,
    author="René Rohner(Snooz82)",
    author_email="snooz@posteo.de",
    description="A library for Data-Driven Testing.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Snooz82/robotframework-datadriver",
    package_dir={"": "src"},
    packages=find_packages("src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Framework :: Robot Framework",
    ],
    install_requires=["robotframework >= 4.0.2, < 8.0", "docutils", "Pygments"],
    extras_require={"xls": ["pandas", "xlrd >= 1.2.0", "openpyxl"]},
    python_requires=">=3.8.0",
)
