#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: html.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-12-14 11:25:47 (CST)
# Last Update:星期五 2016-12-16 9:43:14 (CST)
#          By:
# Description:
# **************************************************************************
import os
from datetime import datetime

from fabric.api import (task, local, put, cd, run, lcd)
from fabric.contrib import files
from fabric.state import env

from .helper import empty_folder
from .helper import overwrite_template

from .fs import mkdir

__all__ = ['delete', 'backup', 'pack', 'putcode', 'activate',
           'local_configure']


@task
def delete(path='output'):
    '''
    前端删除原文件
    '''
    project_path = env.PROJECT_PATH
    with cd(project_path):
        if not empty_folder(project_path):
            run("""ls -l | grep -v logs | awk '{system("rm -rf "$9)}'""",
                warn_only=False)


@task
def backup(path='output'):
    '''
    前端代码备份
    '''
    project_path = env.PROJECT_PATH
    with cd(project_path):
        name = '%s-%s.tar.gz' % (
            env.PROJECT, datetime.now().strftime('%Y-%m-%d-%H'))
        run('tar zcf %s --exclude logs* '
            '--exclude *.tar.gz .' % name, warn_only=True)
    backup_path = '~/backup/html/'
    if not files.exists(backup_path, verbose=True):
        run('mkdir -p %s' % backup_path)
    with cd(project_path):
        run('cp -f %s %s' % (name, backup_path))
        run('rm %s' % name)


@task
def putcode(path='output'):
    '''
    前端代码上传
    '''
    lproject_path = env.LPROJECT_PATH
    project_path = env.PROJECT_PATH
    tar_path = os.path.join(lproject_path, path)
    with lcd(tar_path):
        put('%s.tar.gz' % env.PROJECT, project_path)


@task
def pack(path='output'):
    '''
    前端代码打包
    '''
    lproject_path = env.LPROJECT_PATH
    tar_path = os.path.join(lproject_path, path)
    with lcd(lproject_path):
        local('fis3 release clear')
        local('fis3 release -d %s' % path)
    with lcd(tar_path):
        dirs = os.listdir(tar_path)
        results = []
        for i in dirs:
            if os.path.isdir(os.path.join(tar_path, i)):
                i = i + '/'
            results.append(i)
        results = ' '.join(results)
        local('tar zcf %s.tar.gz --exclude *.tar.gz ' % env.PROJECT + results)


@task
def local_configure(name=None, keep_trailing_newline=False):
    '''
    本地配置文件更新(name=None)
    '''
    if name is not None:
        config = env.LPROJECT_CONF[name]
        overwrite_template(keep_trailing_newline, **config)
    else:
        configs = env.LPROJECT_CONF
        for name, config in configs.items():
            overwrite_template(keep_trailing_newline, **config)


@task
def activate(path='output'):
    '''
    前端类
    '''
    print('正在环境配制')
    local_configure()
    print('正在打包·····')
    pack(path)
    print('正在备份代码·····')
    backup(path)
    print('正在删除代码·····')
    delete(path)
    print('正在上传代码·····')
    putcode(path)
    with cd(env.PROJECT_PATH):
        run('tar zxf %s.tar.gz' % env.PROJECT)
        run('rm %s.tar.gz' % env.PROJECT)
    mkdir()
    print('部署成功····!')
