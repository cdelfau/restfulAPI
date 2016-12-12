import urllib2, json, os

from flask import Flask, render_template, request, session, redirect, url_for
from flask import current_app as app

def get():
    with app.app_context():
        key = app.config["LASTFM_KEY"]
    url = "http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=%s&format=json&page=2&limit=50" % (key)
    u = urllib2.urlopen(url)
    response = u.read()
    data = json.loads( response )
    tracks = []
    for i in range(0,10):
        track =  data['tracks']['track'][i]['name'].encode("utf-8")
        artist = data['tracks']['track'][i]['artist']['name'].encode("utf-8")
        tracks.append(track + " by " + artist)
    return tracks
