#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: deploy.py
# Author: jianglin
# Email: jianglin@1b2b.com
# Created: 2016-10-10 16:42:57 (CST)
# Last Update:星期四 2016-12-15 14:49:57 (CST)
#          By: jianglin
# Description: 部署
# **************************************************************************
from fabric.api import (parallel, task)
from fabric.state import env
from . import git, supervisor, nginx, fs, package

__all__ = [
    'deploy', 'update', 'rollback', 'restart', 'deplhtml2', 'list_roles', 'command'
]


@task(default=True)
@parallel(30)
def deploy(branch=None, commit=None, use_git='True'):
    '''
    部署代码(branch=None, commit=None, use_git=True)
    '''
    use_git = (use_git == 'True')
    if use_git:
        git.activate(branch, commit)
    package.activate()
    fs.activate()
    nginx.activate()
    supervisor.activate()


@task
def rollback(branch=None, commit=None):
    '''
    版本回退(branch=None, commit=None)
    '''
    git.checkout(branch, commit)
    supervisor.restart()


@task
def update(branch=None):
    '''
    更新代码(branch=None)
    '''
    git.pull(branch)
    supervisor.restart()


@task
def restart(name=None):
    '''
    重启服务(name=None)
    '''
    supervisor.restart(name)


@task
def command(cmd='', sudo='False'):
    '''
    发送命令(cmd='',sudo=False)
    '''
    from fabric.contrib.console import confirm
    from fabric.api import sudo as do
    from fabric.api import run
    sudo = True if sudo == 'True' or sudo == '1' else False
    print('command:', cmd)
    if cmd and confirm("You have confirm excute this"):
        if sudo:
            do(cmd)
        else:
            run(cmd)


@task
def list_roles():
    '''
    列出所有role
    '''
    for k, v in env.roledefs.items():
        print(k, v)


@task
def deploy_html(path='output'):
    '''
    前端代码部署(path='output')
    '''
    from . import html
    html.activate(path)
