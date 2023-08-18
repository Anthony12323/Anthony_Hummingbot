#!/usr/bin/env python
#-*- coding: utf-8 -*-
# redis connect pool

import redis

class redisPool:
    # _instance   = None
    _pool       = None
    _r          = None

    # def __new__(cls, *args, **kwargs):
    #     if not cls._instance:
    #         cls._instance = super(redisPool, cls).__new__(cls, *args, **kwargs)
    #     return cls._instance

    def __init__(self, **kwargs):
        host            = kwargs.get('host')
        db              = int(kwargs.get('db'))
        port            = int(kwargs.get('port'))
        password        = kwargs.get("password")
        max_connections = int(kwargs.get('connections', None))
        self._pool = redis.ConnectionPool(host=host, port=port, db=db, password=password, max_connections=max_connections)
        self._r    = redis.Redis(connection_pool = self._pool)

    def __call__(self):
        return self._r