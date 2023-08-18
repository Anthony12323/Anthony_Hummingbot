# coding:utf-8
# create by Camel.Luo at 7/17/2014
# 获取uplus 用户 user-agent 及 promotion channel 的相关工具
import logging
import redis

def getUARecord(uid, _redis, index=0):
    if not isinstance(_redis, redis.client.Redis):
        raise KeyError,"_redis is not a redis connection"
    key = "U:ua:{}".format(uid)
    logging.debug("redis: lindex %s %s", key, index)
    ret = _redis.lindex(key, index)
    if not ret:
        return (ret, 0)
    t   = ret.split("::")
    if len(t)==2:
        return tuple(t)
    else:
        return (ret,0)


def getPromoChannel(mac, idfa, _redis):
    """
    根据mac或idfa获取推广渠道名称
    _redis 必须是记录推广墙数据的redis db 连接
    """
    if not isinstance(_redis, redis.client.Redis):
        raise KeyError,"_redis is not a redis connection"
    udid = mac or idfa
    if not udid:
        return None,None
    key = "hAwakeD:{}".format(udid)
    logging.debug("redis: hmget %s %s", key, 'channel')
    channel, awake_t = _redis.hmget(key, 'channel', 'awake_t')
    return channel,awake_t