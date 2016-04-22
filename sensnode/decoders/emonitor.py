#!/usr/bin/python2
# -*- coding: utf-8 -*-
import time
import datetime
import inspect
import simplejson as json



def emonitor(data):
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

    a = float(data[2]) # temperatura
    b = float(data[4]) # napiecie baterii
    c = float(data[20]) # napiecie sieci 
    d = float(data[6]) # prad 1 
    e = float(data[11]) # prad 2  
    f = float(data[16]) # prad 3 
    #g = float(data[21]) # moc czynna 
    #h = float(data[22]) # moc pozorna 
    if data[21] == 'inf' or data[21] == 'ovf' or data[21] == 'nan':
        g = 0
    else:
        g = float(data[21]) # moc czynna 
    if data[22] == 'inf' or data[22] == 'ovf' or data[22] == 'nan':
        h = 0
    else:
        h = float(data[22])
    i = float(data[23]) # zuzycie
    j = abs(int(data[24])) # level 
    #j = data[18] # moc bierna 
    #k = data[19] # moc czynna 
    #l = data[20] # nume fazay 3 
	#d = data[21] # prad 3 
	#n = data[22] # cos fi 3
	#o = data[23] # moc bierna 3
	#p = data[24] # moc czynna 3
	#q = data[25] # napiecie sieci
	#r = data[26] # suma mocy biernej
	#s = data[27] # suma mocy czynnej
	#t = data[28] # aktualne zuzycie kWh  pomiedzy pomiarami 
	##u = data[29] # przekazniki 
	#w = data[30] # poziom zbiornika 
	#x = data[31]
    #y = data[24]
    #z = data[27] # stan zasilania
	
	#from datetime import datetime
 
    #nodeid = str(data[1])
    name = inspect.stack()[0][3] # z nazwy funcji
    timestamp = int(time.mktime(datetime.datetime.now().timetuple())) # czas unixa
    #name ="Pomiar mocy"
   	#timestamp = int(1364553092)
    template = ({
        'name': name,
        'siec': round (c,2),
        'prad': round ((d + e + f),2),
        'mocb': round (h,2),
        'mocc': round (g,2),
        'zcenazuzycie': round ((i * 0.845745),5),
        'zdzienna': round ((i*1440*0.845745),2),
        'zuzycie': round(i,5),
        'ftank': j,
        'batvol': round(b,3),
        'zzztemp': round(a,2),
        'timestamp':timestamp
         })


    return  dict((k,v) for (k,v) in template.iteritems())
