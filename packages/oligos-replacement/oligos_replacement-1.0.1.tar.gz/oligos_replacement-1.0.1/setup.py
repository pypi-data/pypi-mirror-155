#!/usr/bin/env python3
# -*-coding:Utf-8 -*

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oligos_replacement",
    version="1.0.1",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'pandas'
       ],
    author="Loqmen Anani",
    author_email="loqmen.anani@ens-lyon.fr",
    description="replaces in a genome original sequences by new oligo sequences created for HiC Capture ssDNA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitbio.ens-lyon.fr/LBMC/GM/oligos-replacement",
    classifiers=[
	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': ['oligos_replacement=oligos_replacement.replacement:main'],
    }
)
