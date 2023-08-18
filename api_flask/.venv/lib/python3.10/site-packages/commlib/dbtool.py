#coding:utf-8
import logging
import re

from storage.mysql import connPool

class DBtool:
    _pool_read = None
    _pool_write = None

    def __init__(self, masterconf, slaveconf={}):
        self._pool_write = connPool(**masterconf)
        if slaveconf:
            self._pool_read = connPool(**slaveconf)
        else:
            self._pool_read = self._pool_write

    def query(self, query, *paramenters):
        """执行只读类型的 sql query，list返回执行结果"""        
        if not re.match('select |show ', query , re.I):
            raise Exception("it isn't a read query:"+query)
        dbconn = self._pool_read.db
        logging.debug(query, *paramenters)        
        return dbconn.query(query,*paramenters)

    def iter(self, query, *paramenters):
        """Returns an iterator for the given query and parameters."""        
        if not re.match('select |show ', query , re.I):
            raise Exception("it isn't a read query:"+query)
        dbconn = self._pool_read.db        
        logging.debug(query, *paramenters)        
        return dbconn.iter(query,*paramenters)

    def get(self, query, *paramenters):
        """返回查询结果的第一行"""
        if not re.match('select |show ', query , re.I):
            raise Exception("it isn't a read query:"+query)
        dbconn = self._pool_read.db
        logging.debug(query, *paramenters)        
        return dbconn.get(query,*paramenters)

    def save(self, query, *paramenters):
        """执行写类型的 sql query"""        
        dbconn = self._pool_write.db
        logging.debug(query, *paramenters)        
        return dbconn.execute(query,*paramenters)

    @classmethod
    def dict2set_expr(self, d):
        '''
        dict2set_expr(dict) -> ('key1=%s,key2=%s,....',(val1,val2,...))
        '''
        lcol = []
        lvalues = []
        col_str = ''
        for k,v in d.items():
            if v:
                lcol += ['{}=%s'.format(k)]
                lvalues += [v]
        col_str = ','.join(lcol)
        return (col_str, tuple(lvalues))

    @classmethod
    def dict2and_condition(self, d):
        '''
        dict2and_condition(dict) -> ('key1=%s AND key2=%s AND ..',(val1,val2,...))
        '''
        lcol = []
        lvalues = []
        col_str = ''
        for k,v in d.items():
            if v:
                lcol += ['{}=%s'.format(k)]
                lvalues += [v]
        col_str = ' AND '.join(lcol)
        return (col_str, tuple(lvalues))

