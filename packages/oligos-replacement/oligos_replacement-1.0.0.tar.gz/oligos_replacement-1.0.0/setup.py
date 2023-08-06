#!/usr/bin/env python3
# -*-coding:Utf-8 -*

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oligos_replacement",
    version="1.0.0",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'pandas',
        'Bio.Seq'
    ],
    author="Loqmen Anani",
    author_email="loqmen.anani@ens-lyon.fr",
    description="replaces in a genome original sequences by new oligo sequences created for HiC Capture ssDNA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitbio.ens-lyon.fr/LBMC/RMI2/flexi_splitter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': ['oligos_replacement=oligos_replacement.replacement:main'],
    }
)
