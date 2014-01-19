#!/usr/bin/python2
# -*- coding: utf-8 -*-

import redis
import leveldb
import time
import simplejson as json
import hashlib
import random

import common
import logging
import config

"""
Redis DB szablon:
- hash initv: dane chwilowe z czujek
- kanał nodes(domyślnie) - pubsub
- hash status: dane chwilowe przekaźników
"""


class redisdb():

    """Bazy Redis dla danych chwilowych"""
    def __init__(self, debug=True):
        self.initdb()
        self.debug = debug

    def initdb(self, host="localhost", port=6379):
        self.rdb = redis.Redis(host, port)

    def pubsub(self, data, channel='nodes'):
        if data:
            data_str = json.dumps(data)
            self.rdb.hset("initv", data['name'], data_str)  # hash, field, data
            self.rdb.publish(channel, data_str)
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
    def __init__(self):
        pass

    def slice(self):
        pass