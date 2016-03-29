#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
#wundergroundcom
api = 'f86d1e8be4de0136'
STIMAZOWIE117='http://api.wunderground.com/api/'+ api +'/conditions/q/pws:IMAZOWIE117.json'
STIWARSZAW408='http://api.wunderground.com/api/'+ api +'/conditions/q/pws:IWARSZAW408.json'

def getWeather(station):
    try:
        jsonWeather = requests.get(station)
        return jsonWeather.json()['current_observation']
    except KeyError:
        pass

STATION1 = getWeather(STIMAZOWIE117)
STATION2 = getWeather(STIWARSZAW408)
#mm / h  
try:
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
finally:
    print precip_1hr , precip_today , wind , solarradiation, wind_degrees

