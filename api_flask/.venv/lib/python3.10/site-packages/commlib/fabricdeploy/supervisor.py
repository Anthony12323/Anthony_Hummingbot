#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: supervisor.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-10 15:12:35 (CST)
# Last Update:星期四 2016-12-15 14:28:21 (CST)
#          By:
# Description:
# **************************************************************************
from fabric.state import env
from fabric.api import sudo
from fabric.contrib import files
from fabric.api import task
from .helper import check

__all__ = ['activate', 'install', 'start', 'stop', 'restart', 'update']


def command(cmd):
    sudo(cmd)


def is_installed():
    if files.exists('/usr/bin/supervisord'):
        return True
    return False


def is_running():
    if files.exists('/tmp/supervisor.sock'):
        return True
    return False


@task
def activate():
    '''
    supervisor类
    '''
    if not is_installed():
        install()
    start()


@task
def install():
    '''
    安装supervisor
    '''
    supervisor_conf = env.SUPERVISOR_CONF
    cmd = 'pip2 install supervisor && echo_supervisord_conf > /etc/supervisord.conf && mkdir -p /etc/supervisor/conf.d'
    command(cmd)
    files.append(
        supervisor_conf,
        '[include]\nfiles = /etc/supervisor/conf.d/*.conf',
        use_sudo=True,
        partial=False,
        escape=True,
        shell=False)


@task
def start(name=None):
    '''
    启动supervisor
    '''
    if not is_running():
        cmd = 'supervisord -c %s' % env.SUPERVISOR_CONF
        command(cmd)
        cmd = 'supervisorctl -c %s reload' % env.SUPERVISOR_CONF
        command(cmd)
    else:
        update()
        restart(name)


@task
def stop(name=None):
    '''
    停止supervisor
    '''
    if name is None:
        name = env.SUPERVISOR_NAME
        if check('SUPERVISOR_PROCESS'):
            name = name + ':'
    cmd = 'supervisorctl stop %s' % name
    command(cmd)


@task
def update():
    '''
    更新supervisor配置
    '''
    cmd = 'supervisorctl reread && supervisorctl update'
    command(cmd)


@task()
def restart(name=None):
    '''
    重启supervisor
    '''
    if name is None:
        name = env.SUPERVISOR_NAME
        if check('SUPERVISOR_PROCESS'):
            name = name + ':'
    cmd = 'supervisorctl restart %s' % name
    command(cmd)
