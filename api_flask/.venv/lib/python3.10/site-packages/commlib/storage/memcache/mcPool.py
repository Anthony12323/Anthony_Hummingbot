#!/usr/bin/env python
#-*- coding: utf-8 -*-
# memcache conn 类

import memcache
import logging

import config


serverHash = lambda key : ord(key[-1:])
def mcHash(key):
    hashint = ord(key[-1:])
    logging.debug('memcache key:%s hash:%s' % (key,hashint))
    return hashint
#覆盖 python-memcache 的server Hash 算法函数
memcache.serverHashFunction = mcHash

class memPool():

    def __init__(self, servers, connections=1):
        connections     = int(connections)
        self.pool       = []
        self.pool_size  = connections
        self._mem_index = 0
        for i in xrange(self.pool_size):
            mem_cli = memcache.Client(servers, debug=0)
            self.pool.append(mem_cli)

    @property
    def mc(self):
        if self._mem_index == self.pool_size-1: 
            self._mem_index = 0
        else:
            self._mem_index = self._mem_index + 1
        return self.pool[self._mem_index]


def getPool():
    mcPool = memPool(config.memcache.user_server_list.values(), connections=20)
    return mcPool