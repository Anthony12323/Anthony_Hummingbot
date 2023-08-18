#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-08-01

@author: Devin
"""

import os

from commlib.config import config

_conf_file_path = os.path.abspath(os.path.dirname(__file__)) + "/"
log = config(_conf_file_path + "log.ini", raw=True)