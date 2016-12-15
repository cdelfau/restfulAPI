import urllib2, json, os, random

from flask import Flask, render_template, request, session, redirect, url_for
from flask import current_app as app

#May put in two of the same song rarely: ~1/450 .22%
def get():
    tracks = []
    with app.app_context():
        key = app.config.get("LASTFM_KEY")
    for i in range (0,2):
        page = random.randint(2,10)
        url = "http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=%s&format=json&page=%d" % (key,page)
        u = urllib2.urlopen(url)
        response = u.read()
        data = json.loads( response )
        obj =  data['tracks']['track']
        chosenI = []
        for i in range(0,5):
            ind = None
            while ind == None or ind in chosenI:
                ind = random.randint(0,len(obj)-1)
            chosenI.append(ind)
            print "INDEX: " + str(ind)
            track =  obj[ind]['name'].encode("utf-8")
            artist = obj[ind]['artist']['name'].encode("utf-8")
            tracks.append(track + " by " + artist)
    return tracks
