#!/usr/bin/python2
# -*- coding: utf-8 -*-
import time
import datetime
import inspect
import simplejson as json
import sys


def piec(data):
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
    c = float(data[7]) # bater 
    a = float(data[2]) #gaz 
    b = float(data[3]) # wilgotnosc 
    f = float(data[4]) # temp 
    d = float(data[5]) # cisnienie  
    e = float(data[6]) # stan 
    g = float(data[8]) # ilosc cz. ds 
    h = float(data[9]) # ds1
    i = float(data[10]) # ds5 
    j = float(data[11]) # ds2 
    k = float(data[12]) # ds3 
    l = float(data[13]) # ds4 
    m = int(data[14]) # ilosc. przek
    p = int(data[15])# p1
    o = int(data[16]) # p2
    n = int(data[17]) # p3
    #q = float(woda_last) # napiecie sieci
    #r = int(data[19]) # suma mocy biernej
    #s = data[20] # suma mocy czynnej
    #t = data[28] # aktualne zuzycie kWh  pomiedzy pomiarami 
    ##u = data[29] # przekazniki 
    #w = data[30] # poziom zbiornika 
    #x = data[31]
    #y = data[24]
    #z = data[27] # stan zasilania
    
    #from datetime import datetime
 
    #nodeid = str(data[1])
    name = inspect.stack()[0][3] # z nazwy funcji
    #print "test from decoder:" , name
    timestamp = int(time.mktime(datetime.datetime.now().timetuple())) # czas unixa
    #name ="Pomiar mocy"
    #timestamp = int(1364553092)
    
    template = ({
        'name': name,
        'batvol': c,   #f
        'temp': f,     #c
        'temp1ds': h,  #Temp. boiler
        'temp2ds': j,  #Temp. wejścia solar.
        'temp3ds': k,  #Temp. powrot solar.
        'temp4ds': l,  #Temp. wyj. piec
        'temp5ds': i,  #Temp. pow. piec
        'trela1': int(p),
        'trela2': int(o),
        'trela3': int(n),
        'cis':(d + 8.00),
        'twilg': b,
        'powietrze': round((a / 10.0),2),
        'timestamp':timestamp
        })


    return  dict((k,v) for (k,v) in template.iteritems())

    