#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2016 jianglin
# File Name: git.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2016-10-10 13:38:54 (CST)
# Last Update:星期二 2016-12-6 16:1:29 (CST)
#          By:
# Description:
# **************************************************************************
from fabric.state import env
from fabric.operations import run
from fabric.contrib import files
from fabric.api import task, cd
from .helper import check

__all__ = ['activate', 'clone', 'pull', 'checkout']


def _with_git():
    git_server = '%s:%s/%s.git' % (env.GIT_SERVER, env.PROJECT_OWNER,
                                   env.PROJECT)
    return git_server


def _with_http():
    git_server = env.GIT_SERVER
    if check('GIT_USER'):
        git_server = env.GIT_SERVER.replace('//', '//%s@' % env.GIT_USER)
    if check('GIT_USER') and check('GIT_PASSWORD'):
        git_server = env.GIT_SERVER.replace('//', '//%s:%s@' %
                                            (env.GIT_USER, env.GIT_PASSWORD))
    git_server = '%s/%s/%s.git' % (git_server, env.PROJECT_OWNER, env.PROJECT)
    return git_server


def gen_git_server():
    if env.GIT_SERVER.startswith('http'):
        return _with_http()
    else:
        return _with_git()


def command(cmd):
    run(cmd)


@task
def activate(branch, commit):
    '''
    git类
    '''
    project_path = env.PROJECT_PATH
    if not files.exists(project_path, verbose=True):
        with cd(env.PROJECT_ROOT_PATH):
            clone()
    with cd(project_path):
        checkout(branch, commit)
        pull(branch)


@task
def clone():
    '''
    git clone
    '''
    project_path = env.PROJECT_PATH
    with cd(env.PROJECT_ROOT_PATH):
        if not files.exists(project_path, verbose=True):
            cmd = 'git clone %s' % gen_git_server()
            command(cmd)


@task
def pull(branch=None):
    '''
    git pull origin <branch>
    '''
    project_path = env.PROJECT_PATH
    with cd(project_path):
        if branch is None:
            branch = env.GIT_BRANCH
        cmd = 'git pull origin %s' % branch
        command(cmd)


@task
def checkout(branch=None, commit=None):
    '''
    git checkout <branch> or git reset <commit>
    '''
    project_path = env.PROJECT_PATH
    with cd(project_path):
        if branch is None:
            branch = env.GIT_BRANCH
        cmd = 'git checkout %s' % branch
        command(cmd)
        if commit is not None:
            cmd = 'git reset %s' % commit
            command(cmd)
