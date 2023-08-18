#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: virtualenv.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-10 14:41:35 (CST)
# Last Update:星期二 2016-12-6 16:3:7 (CST)
#          By:
# Description:
# **************************************************************************
from fabric.state import env
from fabric.api import run, task, sudo, cd
from fabric.contrib import files
from fabric.context_managers import prefix
from contextlib import contextmanager
import os

__all__ = ['activate', 'install', 'deactivate', 'mkvirtualenv', 'rmvirtualenv']


def is_created(name):
    venv_path = os.path.join(env.VIRTUALENV_WORK_HOME, name, 'bin', 'activate')
    if files.exists(venv_path, verbose=True):
        return True
    return False


def venv_is_installed():
    if files.exists('/usr/bin/virtualenv', verbose=True):
        return True
    return False


def venvwrapper_is_installed():
    if files.exists('/usr/bin/virtualenvwrapper.sh', verbose=True):
        return True
    return False


@task
def install():
    '''
    安装虚拟环境
    '''
    if not venv_is_installed():
        sudo('pip install virtualenv')
    if not venvwrapper_is_installed():
        sudo('pip install virtulenvwrapper')
        txt = 'export WORKON_HOME=$HOME/.Envs\n \
               export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2\n \
               source /usr/bin/virtualenvwrapper.sh'

        files.append(
            '~/.bash_profile',
            txt,
            use_sudo=False,
            partial=False,
            escape=True,
            shell=False)
        with cd('~/'):
            run('source .bash_profile')


@task
@contextmanager
def activate():
    '''
    激活虚拟环境
    '''
    if not is_created(env.VIRTUALENV_NAME):
        mkvirtualenv()
    with (prefix('workon %s' % env.VIRTUALENV_NAME)):
        yield


@task
def deactivate():
    '''
    退出虛擬環境
    '''
    run('deactivate')


@task
def mkvirtualenv(name=None):
    '''
    創建虛擬環境
    '''
    if name is None:
        name = env.VIRTUALENV_NAME
    cmd = env.VIRTUALENV_COMMAND
    run('%s %s' % (cmd, name))


@task
def rmvirtualenv(name=None):
    '''
    删除虚拟环境
    '''
    if name is None:
        name = env.VIRTUALENV_NAME
    run('rmvirtualenv %s' % name)
