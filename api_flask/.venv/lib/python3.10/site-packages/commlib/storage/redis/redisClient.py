'''
Created on Sep 13, 2012

@author: root
'''
        
from redis.client import Redis
import config

host = config.redis.redis_conn.get("host")
port = int(config.redis.redis_conn.get("port"))
db = config.redis.redis_conn.get("db")
password = config.redis.redis_conn.get("password", None)
        
redis_cli  = Redis(host=host, port=port, db=db, password=password)

host = config.redis.redis_main.get('host')
port = int(config.redis.redis_main.get('port'))
db = config.redis.redis_main.get('db')
password = config.redis.redis_conn.get("password", None)

redis_main = Redis(host=host, port=port, db=db, password=password)