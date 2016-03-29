#!/usr/bin/python2
# -*- coding: utf-8 -*-

import redis
# https://plyvel.readthedocs.org
import plyvel as leveldb
import os
import ast
import time
import simplejson as json

import common
import logging
import config
from itertools import islice

"""
Redis DB szablon:
- hash initv: dane chwilowe z czujnikow
- kanał nodes(domyślnie) - pubsub
- hash status: dane chwilowe przekaźników
"""


class redisdb():

    """Temporary data"""
    def __init__(self, debug=True):
        self.initdb()
        self.debug = debug

    def initdb(self, host="localhost", port=6379):
        self.rdb = redis.Redis(host, port)

    def pubsub(self, data, channel='nodes'):
        if data:
            data_str = json.dumps(data)
            self.rdb.set("initv", data)  # name, value
            self.rdb.publish(channel, data)  # channel, value
            if self.debug:
                logging.debug('Data publish on channel')
                logging.debug('Submit init values')

    def setStatus(self, msg):
        """{"name": "relaynode", "status": 0, "cmd": 1}"""
        jmsg = json.loads(msg)
        self.rdb.hset('status', jmsg['name'] + "_" + jmsg['cmd'], str(msg))

    def getStatus(self, nodename):
        return self.rdb.hget("status", nodename)


class history():

    '''Store data in base for future use ie. graphs'''
    def __init__(self, path, dbname):
        self.path = path
        self.dbname = dbname
        #self.create_db = create_db

        dirname = self.path + "/" + self.dbname

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        self.lvldb = leveldb.DB("%s/%s" % (self.path,
                                        self.dbname),
                                        create_if_missing=True)
        self.dbconnected = True

    def is_connected(self):
        return self.dbconnected

    def get(self, nodename, timerange):

        ranges = {'1h' : 3600,
                '8h' : 28000,
                'day' : 86400,
                '2d': 172800,
                '3d': 259200,
                '4d': 345600,
                '5d': 432000,
                'week' : 604800,
                '2w' : (2 * 604800),
                '3w' : (3 * 604800),
                'month' : 2592000,
                '2m' : (5184000),
                '3m' : (7776000),
                '4m' : (7776000 + 2592000),
                '5m' : (7776000 + 2592000 + 2592000),
                '6m' : (15552000),
                '7m' : (15552000 + 2592000),
                '8m' : (15552000 + 2592000 + 2592000),
                '9m' : (15552000 + 2592000 + 2592000 + 2592000),
                'year' : (31104000)}

        if self.dbconnected:
            data = []
            ts = int(time.time())
            start_key = '%s-%s' % (nodename, ts-ranges[timerange])
            stop_key = '%s-%s' % (nodename, ts)
            
            iterator = self.lvldb.iterator(start=(start_key).encode('ascii'),
                                            stop=(stop_key).encode('ascii'),
                                            include_start=True,
                                            include_stop=True)
                                            
            data = [value for key, value in iterator]
            
            iterator.close()
            if (ts - ranges[timerange]) > (ts - 604900):
                #print 'week'
                return data
            elif(ts - ranges[timerange]) < (ts - 604900) and (ts - ranges[timerange]) > (ts - 2593000):
                data_filtered = [value for value in (islice(data,0,len(data), 10))]
                #print 'month - 3month'
                return data_filtered
            elif (ts - ranges[timerange]) < (ts - 2593000):
                #print 'above 3month'
                data_filtered = [value for value in (islice(data,0,len(data), 100))]
                return data_filtered
    def put(self, key, value):
        if self.dbconnected:
            self.lvldb.put(key, value)
            
    
    def pritndb(self,node):
        
        if self.dbconnected:
            imput = node
            file = open("/mnt/data/"+imput+"_data_node.log", "w")
            for key, value in self.lvldb.iterator(prefix=imput):
                file.write (value)
                file.write("\n")
            file.close()    
        
        return "all database dumped to: /mnt/data/....data_node.log node: %s" % imput
        
    def closeconnectdb(self):
        return self.lvldb.close()
        
    def get_toJSON(self, nodename, sensor, timerange='week'):
        data = []
        if self.dbconnected:
            values = self.get(nodename, timerange)
            # milliseconds for JavaScript
            data = ([[ast.literal_eval(v)['timestamp'] * 1000,ast.literal_eval(v)[sensor]] for (v) in values])
            
            return data
            
            
    def get_toJSON_last(self, nodename, sensor, timerange='1h'):
       data = []
       if self.dbconnected:
           values = self.get(nodename, timerange)
           # milliseconds for JavaScript
           #data = [[ast.literal_eval(v)['timestamp'] *1000, ast.literal_eval(v)[sensor]] for v in values]
           data = [ ast.literal_eval(v)[sensor] for v in values]
           
           return data[-1], data[0]