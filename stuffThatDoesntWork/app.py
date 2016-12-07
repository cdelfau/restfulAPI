import os
import nyct_subway_pb2 #for reading GTFS data from MTA
import gtfs_realtime_pb2
import urllib
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    feed = gtfs_realtime_pb2.FeedMessage()
    response = urllib.urlopen('http://web.mta.info/status/serviceStatus.txt')
    feed.ParseFromString(response.read())
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            print entity.trip_update

    
    # Generate and store secret key if it doesn't already exist
    with open(".secret_key", "a+b") as f:
        secret_key = f.read()
        if not secret_key:
            secret_key = os.urandom(64)
            f.write(secret_key)
            f.flush()
        app.secret_key = secret_key

    app.debug = True
    app.run()
