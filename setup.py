import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robotframework-datadriver",
    version="0.0.1",
    author="René Rohner(Snooz82)",
    author_email="",
    description="A library for data driven tests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Snooz82/robotframework-datadriver",
    package_dir={'':'src'},
    packages=setuptools.find_packages('src'),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Framework :: Robot Framework",
    ],
)
