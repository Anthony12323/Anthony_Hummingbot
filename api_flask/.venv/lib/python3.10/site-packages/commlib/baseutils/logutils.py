#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@date: 2016-08-01

@author: Devin
"""

import logging
import logging.handlers

try:
    from config import log as logconfig
except ImportError:
    from commlib.initconfig import log as logconfig

log = logconfig.log
format = logging.Formatter(log["format"])
level = log['level']
console = log['console'] == "True"


def getLogger(name):
    """
    :param name: 日志文件全路径
    :return:
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    file_handle = logging.handlers.RotatingFileHandler(name)
    file_handle.setFormatter(format)
    file_handle.setLevel(level)
    logger.addHandler(file_handle)
    logger.setLevel(level)

    if console:
        console_handle = logging.StreamHandler()
        console_handle.setFormatter(format)
        console_handle.setLevel(level)
        logger.addHandler(console_handle)
    return logger


if __name__ == "__main__":
    a_log = getLogger("test.log")
    a_log.info("aaaa")
    a_log = getLogger("bbb.log")
    a_log.info("bbb")