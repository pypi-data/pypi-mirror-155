
# File: setup.py 
# Author(s): Vedant Sanil
# Created: Wed Feb 17 11:49:20 EST 2022 
# Description:
# Acknowledgements:
# Copyright (c) 2022 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

import io
import os
import sys
import shutil
import setuptools
import subprocess
from glob import glob
from distutils.command.build_py import build_py

from autonml import __VERSION__

NAME = 'autonml'
VERSION = __VERSION__

with io.open('README.md', 'r', encoding="utf-8") as fp:
    description = fp.read()

with open('requirements.txt', 'r') as reqfile:
    req = [line.strip() for line in reqfile if line and not line.startswith('#')]

def run(args):
    subprocess.run(args, stdout=sys.stdout, stderr=sys.stdout, check=True, encoding='utf8')
    sys.stdout.flush()

pkgs = [elem.replace('autonml/', '') for elem in glob('autonml/static/*', recursive=True) if os.path.isfile(elem)]

setuptools.setup(
    name=NAME,
    version=VERSION,
    install_requires=req,
    url='https://gitlab.com/sray/cmu-ta2/-/tree/dev',
    description=r"AutonML : CMU's AutoML System",
    long_description=description,
    package_data={NAME:pkgs},
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'autonml_main=autonml.main:main_run',
            'automl_search=autonml.main:main_search',
            'create_d3m_dataset=autonml.create_d3m_dataset:main']},
    python_requires=">=3.6",
    include_package_data=True,
    author='Saswati Ray, Andrew Williams, Vedant Sanil',
    maintainer='Andrew Williams, Vedant Sanil',
    maintainer_email='awillia2@andrew.cmu.edu, vsanil@andrew.cmu.edu',
    keywords=['datadrivendiscovery', 'automl', 'd3m', 'ta2', 'cmu'],
    license='Apache-2.0',
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering']
)