#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: file.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-20 15:52:18 (CST)
# Last Update:星期四 2016-12-15 14:50:28 (CST)
#          By:
# Description:
# **************************************************************************
import copy

from fabric.state import env
from fabric.api import run, task
from fabric.contrib import files
from .helper import check, overwrite_template
import os

__all__ = ['activate', 'mkdir', 'configure', 'local_configure']


@task
def activate():
    '''
    配置类
    '''
    if check('ASSERT_DIRECTORY_EXIST'):
        mkdir()
    configure()


def upload_template(name, config):
    filename = config['filename']
    template_dir = config['template_dir']
    destination = config['destination']
    context = copy.copy(config['context'])
    use_jinja = config['use_jinja']
    use_sudo = config['use_sudo']

    extra_context = config.get("extra_context", {}).get(env.host, {})
    context.update(**extra_context)
    files.upload_template(
        filename=filename,
        destination=destination,
        context=context,
        use_jinja=use_jinja,
        use_sudo=use_sudo,
        template_dir=template_dir)


@task
def mkdir():
    '''
    确认目录存在
    '''
    for name, path in env.ASSERT_DIRECTORY_EXIST.items():
        filename = os.path.join(path, name)
        if not files.exists(filename, verbose=True):
            run('mkdir %s' % filename)


@task
def configure(name=None):
    '''
    上传配置文件(name=None)
    '''
    if name is not None:
        config = env.PROJECT_CONF[name]
        upload_template(name, config)
    else:
        configs = env.PROJECT_CONF
        for name, config in configs.items():
            upload_template(name, config)

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


