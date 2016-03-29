#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
#from bs4 import BeautifulSoup
import json
#wunderground.com

api = 'f86d1e8be4de0136'
STIMAZOWIE117='http://api.wunderground.com/api/'+ api +'/conditions/q/pws:IMAZOWIE117.json'
STIWARSZAW408='http://api.wunderground.com/api/'+ api +'/conditions/q/pws:IWARSZAW408.json'

'''def getAQI():
    city = u'Suwałki-Miejska, Polska'
    html = requests.get('http://aqicn.org/city/poland/bialystok/suwalki-miejska/pl/')
    soup = BeautifulSoup(html.text, "html.parser")
    script = soup.find('script', text=re.compile('var mapStationData'))
    json_text = re.search('({.*}])',script.string, flags=re.DOTALL | re.MULTILINE).group(1)
    json_text = json_text + '}'
    json_data = json.loads(json_text)

    scale = {
            (0,50):u'Dobra',
            (51,100):u'Średnia',
            (101,150):u'Niezdrowe dla wrażliwych osób',
            (151,200):u'Niezdrowe',
            (201,300):u'Bardzo niezdrowe',
            (301,999):u'Niebezpieczny'
    }

    for c in json_data['Poland/Bialystok/Suwa%C5%82ki-Miejska']:
        if c['city'] == city:
            sensor_data = c

#    print "%s: %s" % ("Miasto",  sensor_data['city'])
#    print "%s: %s" % ("Data",  sensor_data['utime'])

    try:
        for s in scale.keys():
            if s[0] <= int(sensor_data['aqi']) <= s[1]:
                aqi = scale[s]
    except ValueError:
            aqi = 'Brak danych'
    finally:
            return {'raw': sensor_data['aqi'], 'title': aqi}
'''

def getWeather(city, units='metric', lang='pl', appid='e03a133fd9094c28922ef5fc159189dc'):
    """
    :params city srt: city name
    """
    
    jsonWeather = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?q=' + city + '&units=' + units + '&lang=' + lang + '&appid=' + appid + '&cnt=6&mode=json')
    return jsonWeather.json()
    

def getWeatherCurrent(station):
    try:
        jsonWeather = requests.get(station)
        return jsonWeather.json()['current_observation']
    except KeyError:
        pass

