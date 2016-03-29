#!/usr/bin/python2
# -*- coding: utf-8 -*-
import time
import datetime
import inspect
import simplejson as json
import sys
sys.path.append("../../")
import sensnode.weather 
#import getWeatherCurrent
api = 'f86d1e8be4de0136'
STIMAZOWIE117='http://api.wunderground.com/api/'+ api +'/conditions/q/pws:IMAZOWIE117.json'
STIWARSZAW408='http://api.wunderground.com/api/'+ api +'/conditions/q/pws:IWARSZAW408.json'

def outdoor(data):

    STATION1 = sensnode.weather.getWeatherCurrent(STIMAZOWIE117)
    STATION2 = sensnode.weather.getWeatherCurrent(STIWARSZAW408)
         
    try:
        #mm / h 
        precip_1hr = round((((float(STATION1['precip_1hr_metric']))+(float(STATION2['precip_1hr_metric'])))/2),2)
        # mm day
        precip_today = round((((float(STATION1['precip_today_metric']))+(float(STATION2['precip_today_metric'])))/2),2)
        #wind speed 
        wind = float(STATION1['wind_kph'])
        #W/m2 naslonecznienie
        solarradiation = int(STATION1['solarradiation'])
        #wind_degrees
        wind_degrees = int(STATION1['wind_degrees'])
    
    except TypeError:
        pass
    except IndentationError:
        pass

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
    e = precip_1hr
    g = precip_today
    i = wind
    j = solarradiation
    k = wind_degrees



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
        'zpreciphr': e,
        'zpreciptoday': g,
        'solarradiation': j,
        'wind': i,
        'winddegrees': k,
        'timestamp':timestamp
         })

    return  dict((k,v) for (k,v) in template.iteritems())