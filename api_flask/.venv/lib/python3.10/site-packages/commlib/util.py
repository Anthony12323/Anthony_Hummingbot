#!/usr/bin/env python
#-*- coding: utf-8 -*- 
#通用工具函数

import logging
from datetime import date, datetime, timedelta
import time
from md5 import md5
from tornado import httpclient
from tornado.options import options
import config
import decimal
import httplib
import json


def resolve_photo_uri(uri,size):
    return None
    lPath = uri.split('/')
    if size != 'origin':
        size_key = "%s_size_alias" % size
        if config.uplus.photo.has_key(size_key):
            size_name = config.uplus.photo[size_key]
            for i in range(len(lPath)):
                if lPath[i] == config.uplus.photo['origin_size_alias']:
                    lPath[i] =  size_name
        else:
            return None
    url = config.uplus.photo['photo_url'].format(uri = "/".join(lPath))
    return url

def get_photo_url(uri, sizes, **setting):
    path = uri.split('/')
    ret  = {}
    for size in sizes:
        skey = '%s_size' % size
        url = ''
        if setting.has_key(skey):
            sname = setting.get(skey)
            path_c = []            
            for value in path:
                if value == setting['swap_word']:
                    path_c.append(sname)
                else:
                    path_c.append(value)
            url = setting.get('photo_url').format(uri = "/".join(path_c))
        ret[size] = url
    return ret

def delete_user_from_mongo(userid):
    url = config.uplus.user_cache.get('mongo_http_url')
    if not url:
        return 0
    url = url.format(user_id=userid)
    if options.debug:
        print url

    def handle_request(res):
        if options.debug:
            print res.code

    http_client = httpclient.AsyncHTTPClient()
    http_client.fetch(url, handle_request, method="DELETE")
    return 1

def get_the_next_day_str(date):
    try:
        tdate = datetime.strptime(date, config.app.date_format)
    except Exception, e:
        return 0
    ndate   = tdate+timedelta(1) 
    return ndate.strftime(config.app.date_format)

def dthandler(obj):
    '''
    将datetime 和 Decimal 类型 parser 为 JSON支持的str类型
    '''
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
    else:
        raise TypeError('%r is not JSON serializable' % obj)

def to_datetime(timestamp):
    """
    将时间戳转换成datetime类型
    如果格式不对，则返回None
    """
    if isinstance(timestamp, datetime):
        return timestamp
    if isinstance(timestamp, str) or isinstance(timestamp, unicode):
        try:
            if timestamp.find('.') > 0:
                timestamp = float(timestamp)
            else:
                timestamp = int(timestamp)        
        except ValueError, e:
            logging.error(ValueError(e))
            return None

    if isinstance(timestamp, float):
        try:
            return datetime.fromtimestamp(timestamp)
        except ValueError, e:
            logging.error(ValueError(e))
            return None
    if isinstance(timestamp, int):
        try:
            return datetime.fromtimestamp(timestamp/1000)
        except ValueError, e:
            logging.error(ValueError(e))
            return None
    logging.error(TypeError('%r is not Correct timestamp' % timestamp))
    return None

def datetime_to_timestamp(dt):
    """
    
    """
    if not isinstance(dt, datetime):
        return None
    return time.mktime(dt.timetuple())

def reverse_dict(dt):
    "转换字典对象的key 和 value"
    return dict(map(lambda t:(t[1],t[0]), dt.items()))

# def send_notice(senderid,receiverid,typeid,content,objectid,resourceid):
#     "给用户发送通知"
#     logging.debug(content)
#     host = config.uplus.send_notice.get("host")
#     port = int(config.uplus.send_notice.get("port"))
#     url =  config.uplus.send_notice.get("url")
#     body = json.dumps({'sender':senderid, 'receiver':receiverid, 'type':typeid, 'content':content, 'object':objectid, 'resource':resourceid})
#     headers = {"Content-type": "application/json",  "Accept": "text/plain"}

#     #异步HttpClient
#     def handle_request(res):
#         logging.debug(res.code)

#     req_url = "http://{host}:{port}/{url}".format(host=host, port=port, url=url)
#     http_client = httpclient.AsyncHTTPClient()
#     request = httpclient.HTTPRequest(url=req_url, headers=headers, body=body, method="POST")
#     logging.debug("SendNotic: url=%s ,headers=%s, body=%s " % (req_url, headers, body))
#     http_client.fetch(request,handle_request)
#     return 1

_date_format = '%Y-%m-%d'
_datetime_format = '%Y-%m-%d %H:%M:%S'

def date_convert(datestr):
    """
    日期字符串转换成datetime对象
    """
    try:
        return datetime.strptime(datestr, _date_format)
    except Exception, e:
        raise e

def datetime_convert(datestr):
    """
    字符串转换成datetime对象
    """
    try:
        return datetime.strptime(datestr, _datetime_format)
    except Exception, e:
        raise e

def count_age(birthday):
    """
    计算年龄
    """
    if not isinstance(birthday, datetime):
        if not isinstance(birthday, date):
            try:
                birthday = date_convert(birthday)
            except ValueError, e:
                try:
                    birthday = datetime_convert(birthday)
                except:
                    return None

    now = datetime.today()
    age = now.year - birthday.year
    if now.month < birthday.month:
        age -= 1
    if now.month == birthday.month and now.day < birthday.day:
        age -= 1

    return age

def zodiac(birthday, suffix=u'座'):  
    """
    计算星座
    """
    if not isinstance(birthday, datetime):
        if not isinstance(birthday, date):
            try:
                birthday = date_convert(birthday)
            except Exception, e:
                return None
    
    month = birthday.month
    day   = birthday.day

    zodiac_map = {  
        u'白羊':[(3,21), (4,20)],  
        u'金牛':[(4,21), (5,20)],  
        u'双子':[(5,21), (6,21)],  
        u'巨蟹':[(6,22), (7,22)],  
        u'狮子':[(7,23), (8,22)],  
        u'处女':[(8,23), (9,22)],  
        u'天秤':[(9,23), (10,22)],  
        u'天蝎':[(10,23), (11,21)],  
        u'射手':[(11,23), (12,22)],  
        u'水瓶':[(1,20), (2,18)],  
        u'双鱼':[(2,19), (3,20)]  
    }  
    for k,v in zodiac_map.iteritems():  
        if v[0] <= (month,day) <= v[1]:  
            return k+suffix  
  
    if (month,day) >= (12,22) or (month,day) <= (1,19):  
        return u'摩羯'+suffix  

def weeksOfyear(day):
    """
    返回日期为当年的第几周
    """
    if not isinstance(day, datetime):
        if not isinstance(day, date):
            try:
                day = date_convert(day)
            except Exception, e:
                return None
    return day.strftime('%W')

def splitUa(ua="-"):
    "拆分UA"
    try:
        ua = ua.replace("'","''")
        ua = ua.replace("\\","\\\\")
        ua = ua.replace("%","%%")            
    except Exception, e:
        return

    if ua == None or ua == '-' : return
    ua = ua.lower()
    uaDetail = {}
    
    if ua.find('#') >=0 :
        ua = ua[:ua.find('#')].replace("-","_") + ua[ua.find('#'):]
    
    # 处理特殊的android 机型ua
    def _addAndroid(ua):
        index = ua.find('-') 
        if index < 0 :
            index = len(ua)
        ua = ua[:index]+"-android"+ua[index:]
        return ua

    # 处理特殊的iphone机型ua
    def _addiPhone(ua):
        index = ua.find('-')
        if index < 0 :
            index = len(ua)
        ua = ua[:index]+"-iphone"+ua[index:]
        return ua

    if ua.find("mx_") == 0:
        ua = _addAndroid(ua)

    if ua.find("longcheer_#") == 0:
        ua = _addAndroid(ua)
    
    if ua.find("yiwap_#")== 0:
        ua = _addAndroid(ua)

    if ua in ('appstore#00bt','uplus#00bv','91zhushou#00el'):
        ua = _addiPhone(ua)

    ua = ua.replace("symbian_","symbian-")
    ua = ua.replace("-#","#",1)
    
    lua = ua.split('-',2)
    
    xlens = 3 - len(lua)
    if xlens > 0:
        lua.extend(['' for i in range(xlens)])

    #如果第一个字段为平台名称，则添加默认渠道uplus至第一位
    if lua[0] in ('iphone', 'android' , 'symbian' , 'mtk' , 'win' , 'unknown' , '') :
        lua = ['uplus']+lua
    #如果第二个字段无法识别为已知平台则划归MTK
    if lua[1] not in ('iphone','android','symbian','mtk' , 'win' , 'unknown') :
        lua.insert(1,"mtk")

    #MTK平台将渠道名称和机型合并为渠道名称
    if lua[1] == "mtk":
        if lua[0].find("#") < 0:
            if lua[2] != '':
                lua[0] += "-%s" % lua[2]
    
    uaDetail['channel'] = lua[0]
    uaDetail['platform'] = lua[1]
    uaDetail['model'] = '-'.join([x for x in lua[2:] if x != '']) 

    return uaDetail

def timeRange(ftime, ttime, st='HOUR'):
    '''
    timestampRange(time, time, ['DAY'|'HOUR'|..]) -> (t1,t2....)
    按天、小时、半小时、一刻钟的间隔 ，返回从 ftime 到 ttime 整点的时间戳序列
    '''
    if ttime<ftime:
        return False
    if st == 'DAY':
        ss = 3600*24
    elif st=='HOUR':
        ss = 3600
    elif st=='HALFHOUR':
        ss = 1800
    elif st == 'QUARTER':
        ss = 900
    else:
        raise ValueError,'error st "%s"' % st
    
    if st=='DAY':
        ftime -= time.timezone
        ttime -= time.timezone
    tf = int(ftime-(ftime%ss))
    tt = int(ttime+(ss-ttime%ss))
    if st=='DAY':
        tf += time.timezone
        tt += time.timezone

    ret = range(tf,tt,ss)+[tt]

    return ret


