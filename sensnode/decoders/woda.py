#!/usr/bin/python2
# -*- coding: utf-8 -*-
import time
import datetime
import inspect
import simplejson as json
import sys
import os
import cPickle as pickle
#sys.path.insert(0,'..')
#from getrelays import checkrelays

def woda(data):
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
#----------------------------------tu  pisac swoje razem z importem na poczatku ---------------------  
 #store = p1,p2,p3,woda_last,(woda_last - woda_first),(cena_woda_last - cena_woda_first),(gaz_last - gaz_first), (cena_gaz_last - cena_gaz_first)
    pickledir = os.path.abspath((os.path.dirname(__file__)) + '/../../cpickle')
    picklefile = 'datarelay.pic'
    openpicklefileread = open(pickledir + '/' + picklefile, 'rb')
    #print pickledir
    get_data = pickle.load(openpicklefileread)
    openpicklefileread.close()
    w1 = get_data[4]
    w2 = get_data[5]
    w3 = get_data[10]
    a = float(data[2]) #deszcz
    b = float(data[3]) #temperatura
    c = float(data[4]) 
    d = float(data[5])#bateria
    e = float(data[6]) #pomiar woda
    #f = float(sensmon.woda_last) #pomiar woda
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
        'batvol': d,
        'deszcz': int(a * 0.01),
        'zzztemp': b,
        'pulse': e,
        'wop': round ((e * 4.53),2),
        'wor': int(w1*100),
        'wos': round(w2,2),
        'ewob': w3,
        'timestamp':timestamp

        
         })

    #list = pickle.load(sys.stdin)
    #print float(item)
    
    return  dict((k,v) for (k,v) in template.iteritems())
