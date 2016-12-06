import urllib2, json, time
from urllib2 import HTTPError


#https://darksky.net/dev/docs/forecast
#https://openweathermap.org/current

#OpenWeatherMap to get coordinates
url = "http://api.openweathermap.org/data/2.5/weather?zip=10282,us"
url += "&APPID=bc5b1b41b7a0cec8b093b8c0271d6ee0"

u = urllib2.urlopen(url)
response = u.read()
owm = json.loads( response )
lat = owm['coord']['lat']
lon = owm['coord']['lon']
print ("LAT: " + lat)
print ("LON: " + lon)

#MAKE SURE TO CONVERT TEMP
#OPENWEATHER IS IN K
#DARK SKY IS IN C


#Dark Sky API  
url2 = "https://api.darksky.net/forecast/fcece9a1ddf04aa5db8b1339edec5e81/"
url2 += ("%s,%s") % (lat,lon)
try: 
    u2 = urllib2.urlopen(url2)


    response2 = u2.read()
    ds = json.loads(response2)


    #summary
    #icon
    #precipProbab
    #temp (also min/max for day and when)
    #humidity
    #windspeed
    #visibility
    #sunrise / sunset


    #minutely or hourly or currently?
    print ds['currently']['summary']
    print ds['currently']['icon']
    print ds['currently']['precipProbability']
    print ds['currently']['precipType']
    print ds['currently']['temperature']
    print ds['daily']['data'][0]['temperatureMin']
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ds['daily']['data'][0]['temperatureMinTime']))
    print ds['daily']['data'][0]['temperatureMax']
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ds['daily']['data'][0]['temperatureMaxTime']))
    print ds['currently']['humidity']       # 0 to 1 scale
    print ds['currently']['visibility']     #in km

except HTTPError: 

    #if darksky reaches limit
    #weather
    #wind
    #temp (and min max)
    #humidity
    #sunrise / sunset

    print (owm['weather'])
    print (owm['wind'])
    print (owm['main']['temp'])
    print (owm['main']['temp_min'])
    print (owm['main']['temp_max'])
    print (owm['main']['humidity'])

    #print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(owm['sys']['sunset'])))
    print (time.strftime('%H:%M:%S', time.localtime(owm['sys']['sunrise'])))
    print (time.strftime('%H:%M:%S', time.localtime(owm['sys']['sunset'])))
