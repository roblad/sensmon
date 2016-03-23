#!/usr/bin/python2
# -*- coding: utf-8 -*-
import time
import datetime
import inspect
import simplejson as json

def outdoor(data):
    '''Pomiar:
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
    '''
    a = float(data[7]) #napiecie  batvol
    f = float(data[2]) #wilg gleby groundhumi
    b = float(data[3]) #wilgotnosc humi
    c = float(data[4]) #temperatura temp
    d = float(data[5]) #naslonecznienie sun
    h = float(data[9]) #temp gleby tempground



    #nodeid = str(data[1])
    name = inspect.stack()[0][3] # z nazwy funcji
    timestamp = int(time.mktime(datetime.datetime.now().timetuple())) # czas unixa

    template = ({
        'name':name,
        'batvol': a,
        'sun': d,
        'thumi': b,
        'temp': c,
        'tgroundhumi': f,
        'tempground': h,
        'timestamp':timestamp
         })

    return  dict((k,v) for (k,v) in template.iteritems())