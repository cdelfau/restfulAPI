import urllib2, json



maps = "https://googleapis.com/geolocation/v1/geolocate?key=AIzaSyDWrKbZzxYmIgwKI2C5VDYh9ljl2__jpsU"
m = urllib2.urlopen(maps)
response = m.read()
dat = json.loads(response)
    
#Dark Sky API  
#url = https://api.darksky.net/forecast/fcece9a1ddf04aa5db8b1339edec5e81/
#url += #lat, long

#OpenWeatherMap if limit reached
url = "http://api.openweathermap.org/data/2.5/weather?zip=10282,us"
url += "&APPID=bc5b1b41b7a0cec8b093b8c0271d6ee0"

u = urllib2.urlopen(url)
response = u.read()
data = json.loads( response )
print (data['weather'])
print (dat["location"])


#get long, lat via zip for open weather map
#or google geolocation api

#summary
#icon
#precipProbab
#temp (also min/max for day and when)
#windspeed
#visibility
#sunrise / sunset

#maybe moon phase




#if darksky reaches limit
#weather
#wind
#temp (and min max)
#sunrise / sunset

