# File: __init__.py 
# Author(s): Vedant Sanil
# Created: Wed Feb 17 11:49:20 EST 2022 
# Description:
# Acknowledgements:
# Copyright (c) 2022 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

"""AutonML package"""

__VERSION_MAJOR__  = '0'
__VERSION_MINOR__ = '2'
__VERSION_BUILD__ = '6'

__VERSION__ = f'{__VERSION_MAJOR__}.{__VERSION_MINOR__}.{__VERSION_BUILD__}'

from autonml.autonml_api import AutonML
from autonml.autonml_api import createD3mDataset
