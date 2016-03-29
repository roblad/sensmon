#!/usr/bin/python2
# -*- coding: utf-8 -*-
import time
import datetime
import inspect
import simplejson as json
import sys
import os
import cPickle as pickle

def gaz(data):
    """Pomiar:
    - swiatła,
    - wlgotności
    - temperatury
    - ciśnienia
    - stanu baterii
    - napięcia beterii

    >> a = "OK 2 0 0 70 1 242 0 201 38 0 15 17"
    >> raw = a.split(" ")
    >> weathernode(raw, "weathernode")
    '{"name": "weathernode", "temp": "242", "lobat": "0", "humi": "326", "timestamp": 1364553092, "light": "0", "press": "9929", "batvol": "4367"}'
        """
#----------------------------------wartosci pickle gaz i cena ---------------------  
    pickledir = os.path.abspath((os.path.dirname(__file__)) + '/../../cpickle')
    picklefile = 'datarelay.pic'
    openpicklefileread = open(pickledir + '/' + picklefile, 'rb')
    get_data = pickle.load(openpicklefileread)
    openpicklefileread.close()
    g1 = get_data[6]
    g2 = get_data[7]


    a = float(data[2]) #temperatura
    b = int(data[3]) 
    c = float(data[4]) #bateria
    d = float(data[5]) #pomiar gaz
    #e = int(data[6])
    #f = int(data[7])
    #g = int(data[8])
    #h = int(data[9])
    #i = int(data[10])
    #j = int(data[11])
    #k = int(data[12])

    #nodeid = str(data[1])
    name = inspect.stack()[0][3] # z nazwy funcji
    timestamp = int(time.mktime(datetime.datetime.now().timetuple())) # czas unixa

    template = ({
        'name':name,
         #'humi': str((256 * d) + c),
        'batvol': c,
        'zzztemp': a,
        'pulse': d,
        'zuzycieoplata' : round((d * 1.97),2),
        'zd' : round(g1,2),
        'zdoplata' : round(g2,2),
        'timestamp':timestamp
         })

    return  dict((k,v) for (k,v) in template.iteritems())
