#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: package.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-21 10:45:32 (CST)
# Last Update:星期四 2016-12-15 14:51:14 (CST)
#          By:
# Description:
# **************************************************************************
from fabric.state import env
from fabric.api import run, task, cd
from fabric.contrib import files
from . import virtualenv
import os

__all__ = ['activate', 'install', 'uninstall']


@task
def activate():
    '''
    package 类
    '''
    require()


@task
def install(name):
    '''
    安装package(name)
    '''
    with virtualenv.activate():
        run('pip install %s' % name)


@task
def uninstall(name):
    '''
    卸载package(name)
    '''
    with virtualenv.activate():
        run('pip uninstall %s' % name)


def require():
    project_path = env.PROJECT_PATH
    requirements = os.path.join(project_path, 'requirements.txt')
    if files.exists(requirements, verbose=True):
        with virtualenv.activate(), cd(project_path):
            run('pip install -r requirements.txt')
