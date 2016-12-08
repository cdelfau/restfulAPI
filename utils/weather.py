import hashlib
import os

from flask import Flask, render_template, request, session, redirect, url_for
from flask import current_app as app

import urllib2, json, time
from urllib2 import HTTPError


#https://darksky.net/dev/docs/forecast
#https://openweathermap.org/current

def getInfo():
    return getInfo(10282)

def getInfo(ZIP):

    info = {}

    ZIP = int(ZIP)

    with app.app_context():
        key1 = app.config["OPENWEATHER_KEY"]
        key2 = app.config["DARKSKY_KEY"]

    #OpenWeatherMap to get coordinates
    url = "http://api.openweathermap.org/data/2.5/weather?zip=%d,us" % (ZIP)
    url += "&APPID=%s" % (key1)
    u = urllib2.urlopen(url)
    response = u.read()
    owm = json.loads( response )
    lat = owm['coord']['lat']
    lon = owm['coord']['lon']

    #MAKE SURE TO CONVERT TEMP
    #OPENWEATHER IS IN K
    #DARK SKY IS IN C

    #Dark Sky API
    url2 = "https://api.darksky.net/forecast/%s/" % (key2)
    url2 += ("%s,%s") % (lat,lon)
    try:
        u2 = urllib2.urlopen(url2)
        response2 = u2.read()
        ds = json.loads(response2)

        info["summaryNow"] = ds['currently']['summary']
        info["summaryHour"] = ds['minutely']['summary']
        info["summaryDay"] = ds['hourly']['summary']
        info['icon'] = ds['currently']['icon']
        info['precipProb'] = ds['currently']['precipProbability']
        try:
            info['precipType'] = ds['currently']['precipType']
        except:
            info['precipType'] = None
        info['temp'] = ds['currently']['temperature']
        info['minTemp'] = ds['daily']['data'][0]['temperatureMin']
        info['maxTemp'] = ds['daily']['data'][0]['temperatureMax']
        info['minTempTime'] = time.strftime('%H:%M:%S', time.localtime(ds['daily']['data'][0]['temperatureMinTime']))
        info['maxTempTime'] = time.strftime('%H:%M:%S', time.localtime(ds['daily']['data'][0]['temperatureMaxTime']))
        info['humidity'] = ds['currently']['humidity']       # 0 to 1 scale
        info['visibility'] = ds['currently']['visibility']     #in km
        info['sunrise'] = time.strftime('%H:%M:%S', time.localtime(ds['daily']['data'][0]['sunriseTime']))
        info['sunset'] = time.strftime('%H:%M:%S', time.localtime(ds['daily']['data'][0]['sunsetTime']))

        return info

    except HTTPError:

        #print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(owm['sys']['sunset'])))

        info["summaryNow"] = [str(owm['weather'][0]['main']),str(owm['weather'][0]['description'])]
        info["summaryHour"] = None
        info["summaryDay"] = None
        info["icon"] = owm['weather'][0]['icon']
        info["precipProb"] = None
        info['precipType'] = None
        info['temp'] = owm['main']['temp']
        info['minTemp'] = owm['main']['temp_min']
        info['maxTemp'] = owm['main']['temp_max']
        info['minTempTime'] = None
        info['maxTempTime'] = None
        info['humidity'] = owm['main']['humidity'] / 100
        info['visibility'] = None
        info['sunrise'] = time.strftime('%H:%M:%S', time.localtime(owm['sys']['sunrise']))
        info['sunset'] = time.strftime('%H:%M:%S', time.localtime(owm['sys']['sunset']))

        return info
