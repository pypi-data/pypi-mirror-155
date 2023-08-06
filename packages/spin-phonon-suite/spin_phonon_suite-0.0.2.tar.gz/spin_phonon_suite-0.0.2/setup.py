#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long,missing-module-docstring,exec-used

import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

# DO NOT EDIT THIS NUMBER!
# IT IS AUTOMATICALLY CHANGED BY python-semantic-release
__version__ = "0.0.2"

setuptools.setup(
    name='spin_phonon_suite',
    version=__version__,
    author='Chilton Group',
    author_email='nicholas.chilton@manchester.ac.uk',
    description='A package for performing spin-phonon coupling calculations with openMOLCAS and Gaussian', # noqa
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://gitlab.com/chilton-group/spin_phonon_suite",
    project_urls={
        "Bug Tracker": "https://gitlab.com/chilton-group/spin_phonon_suite/-/issues", # noqa
        "Documentation": "https://chilton-group.gitlab.io/spin_phonon_suite"
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
        ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'scipy',
        'h5py',
        'xyz_py',
        'angmom_suite',
        'hpc_suite',
        'matplotlib',
        'findiff'
        ],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'spin_phonon_suite = spin_phonon_suite.cli:main'
            ]
        }
    )
