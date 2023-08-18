#coding:utf-8
import logging
from md5 import md5
import base64 

def strCode(string, key='', action='ENCODE'):
    """
    字符串简单加密
    strCode(source_str, key, 'ENCODE') -> encrypt string
    strCode(encrypt_str, key, 'DECODE') -> source string
    """
    string = str(string)
    key    = str(key)
    try:
        string = base64.b64decode(string) if action is not 'ENCODE' else string
    except:
        return None
    code = ""
    key  = md5(key).hexdigest()[7:18] #! don't change the substring's range when service was running
    key_len = len(key)
    str_len = len(string)
    for i in range(str_len):
        k     = i % key_len
        code += chr(ord(string[i]) ^ ord(key[k]))
    ret = action is 'DECODE' and code or base64.b64encode(code)
    return ret 

def hash_password(password, salt):
    return md5(md5(str(password)).hexdigest()+salt).hexdigest()
