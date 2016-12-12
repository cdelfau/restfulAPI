import urllib2, json, os, random

from flask import Flask, render_template, request, session, redirect, url_for
from flask import current_app as app

def get():
    with app.app_context():
        key = app.config["LASTFM_KEY"]
    url = "http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=%s&format=json&page=2&limit=100" % (key)
    u = urllib2.urlopen(url)
    response = u.read()
    data = json.loads( response )
    tracks = []
    chosen = []    
    for i in range(0,10):
        #randomize
        chosen = []
        ran = -1
        while ran in chosen or ran != -1:
            ran = random.randrange(0,100)
        track =  data['tracks']['track'][ran]['name'].encode("utf-8")
        artist = data['tracks']['track'][ran]['artist']['name'].encode("utf-8")
        tracks.append(track + " by " + artist)
        chosen.append(ran)
    return tracks
