from flask import Flask, render_template
import urllib2, json

app = Flask(__name__)


@app.route("/")
def root():
    url = "http://api.openweathermap.org/data/2.5/weather?zip=10282,us"
    url += "&APPID=bc5b1b41b7a0cec8b093b8c0271d6ee0"
    u = urllib2.urlopen(url)
    response = u.read()
    data = json.loads( response )
    return render_template("weatherIndex.html", wea = data['weather'] )


if __name__ == "__main__":
   app.debug = True
   app.run()
