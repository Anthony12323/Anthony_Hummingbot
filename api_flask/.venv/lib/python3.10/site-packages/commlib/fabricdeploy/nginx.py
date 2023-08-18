#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: nginx.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-10 14:33:16 (CST)
# Last Update:星期二 2016-12-6 14:27:33 (CST)
#          By:
# Description:
# **************************************************************************
from fabric.state import env
from fabric.api import sudo
from fabric.contrib import files
from fabric.api import task

__all__ = ['activate', 'start', 'stop', 'reload', 'install']


def command(cmd):
    sudo(cmd)


def is_installed():
    if files.exists('/usr/sbin/nginx', verbose=True):
        return True
    return False


def is_running():
    if files.exists('/var/run/nginx.pid', verbose=True):
        return True
    return False


@task
def activate():
    '''
    nginx类
    '''
    if not is_installed():
        install()
    start()


@task
def start():
    '''
    启动nginx
    '''
    nginx_conf = env.NGINX_CONF
    if not is_running():
        cmd = 'nginx -c %s' % nginx_conf
    else:
        cmd = 'nginx -c %s -s reload' % nginx_conf
    command(cmd)


@task
def stop():
    '''
    停止nginx
    '''
    nginx_conf = env.NGINX_CONF
    cmd = 'nginx -c %s -s stop' % nginx_conf
    command(cmd)


@task
def reload():
    '''
    重载nginx
    '''
    nginx_conf = env.NGINX_CONF
    cmd = 'nginx -c %s -s reload' % nginx_conf
    command(cmd)


@task
def install():
    '''
    安装nginx
    '''
    cmd = 'yum install nginx'
    command(cmd)
