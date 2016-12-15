import hashlib

from flask import Flask, render_template, request, session, redirect, url_for

import config
import setup

from utils import user, weather, transit, topTracks

app = Flask(__name__)

def validate_form(form, required_keys):
    return set(required_keys) <= set(form)

@app.route("/")
def index():
    if "username" in session:
        success, _weather, _transit, zip_code, tracks = autoResult()
        if success:
            return render_template("result.html", weather=_weather, transit=_transit, zip_code=zip_code, tracks=tracks)
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        if not validate_form(request.form, ["username", "password"]):
            return render_template("login.html", message="Malformed request", category="danger")
        form = request.form
        username = form.get("username")
        password = hashlib.sha256(form.get("password")).hexdigest()
        _user = user.get_user(username=username, password=password)
        if _user:
            session["username"] = username
            return redirect(url_for("index"))
        return render_template("login.html", message="Invalid credentials", category="danger")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        if not validate_form(request.form, ["username", "password", "confirm_password"]):
            return render_template("register.html", message="Malformed request", category="danger")
        form = request.form
        username = form.get("username")
        password = form.get("password")
        confirm_password = form.get("confirm_password")
        if password != confirm_password:
            return render_template("register.html", message="Passwords do not match", category="danger")
        _user = user.get_user(username=username)
        if _user:
            return render_template("register.html", message="Username already in use.", category="danger")
        else:
            user.add_user(username, password)
            return render_template("register.html", message="Account created", category="success")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        form = request.form
        try:
            zip_code = int(form.get("zip_code"))
        except:
            return render_template("index.html", message="Malformed request", category="danger")
        if form.get("save"):
            saveSettings(form)
        _transit = {}
        if form.get("subway"):
            _transit["subway"] = transit.getSubwayStatus()

        if form.get("lirr"):
            _transit["lirr"] = transit.getLIRRStatus()

        bus = form.get("bus")
        if bus:
            bus_number = form.get("borough") + form.get("bus_number")
            busStops = transit.stopsOnRoute(bus_number)

            if busStops == None:
                _transit["bus"] = "No such bus route"
            else:
                _transit["bus"] = busStops
            _transit["bus_number"] = bus_number

        _weather = weather.getInfo(zip_code)
        tracks = None
        if session.get("username"):
            tracks = topTracks.get()
        return render_template("result.html", weather=_weather, transit=_transit, zip_code=zip_code, tracks=tracks)
    return ""

def autoResult():
    _transit = {}
    username = session.get("username")
    d = user.get_settings(username)
    zip_code = d.get('zip_code')

    if not zip_code:
        return 0, {}, {}, "", []

    if d.get('subway') == 1:
        _transit['subway'] = transit.getSubwayStatus()
    if d.get('bus') == 1:
        busStops = transit.stopsOnRoute(d['busNum'])
        if busStops == None:
            _transit["bus"] = "No such bus route"
        else:
            _transit["bus"] = busStops
        _transit['bus_number'] = d['busNum']
    if d.get('lirr') == 1:
        _transit['lirr'] = transit.getLIRRStatus()
    _weather = weather.getInfo(zip_code)
    tracks = topTracks.get()
    return 1, _weather, _transit, zip_code, tracks

@app.route("/buses", methods=["GET"])
def bus():
    bus_number = request.args.get("bus")
    stop = request.args.get("stop")
    buses = []
    if stop:
        buses = transit.getBusesRelativeToStop(bus_number, stop)
    return render_template("bus.html", buses=buses)

def saveSettings(form):
    d = {}
    fields = ['zip_code', 'subway', 'bus', 'lirr']
    for field in fields:
        if field in form:
          d[field] = form[field]
    if 'bus' in d:
        d['busNum'] = form['borough'] + form['bus_number']
    user.save_settings(session.get('username'), d)

@app.context_processor
def inject_username():
    """ Inject the username into each template, so we can render the navbar correctly. """
    username = session.get("username")
    if username:
        return dict(username=username)
    return dict()

if __name__ == "__main__":

    setup.initialize_tables()
    app.config.from_object(config)

    app.debug = True
    app.run()
