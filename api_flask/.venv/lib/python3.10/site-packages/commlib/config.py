# coding:utf-8

import os
import sys
from ConfigParser import ConfigParser


class config():
    __cache = {}
    # __filepath = os.path.abspath(os.path.dirname(__file__))+"/"
    __filename = 'config.ini'
    __file = __filename

    def __init__(self, sFile='', raw=False):
        if sFile != '':
            self.__filename = sFile
            self.__file = self.__filename

        config = ConfigParser()
        config.read(self.__file)

        self.__cache = {}
        for section in config.sections():
            self.__cache[section] = {}
            for option in config.options(section):
                self.__cache[section][option] = config.get(section, option,
                                                           raw=raw)

    def __getattr__(self, section):
        if self.__cache.has_key(section):
            return self.__cache[section]
        elif self.__cache.has_key('default'):
            if self.__cache['default'].has_key(section):
                return self.__cache['default'][section]
            else:
                return {}
        else:
            return {}

    def __repr__(self):
        filestring = open(self.__file, 'r').read()
        string = '''Config File: %s
----------
%s
----------
        ''' % (self.__file, filestring)

        return string
