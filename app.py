import hashlib
import os

from flask import Flask, render_template, request, session, redirect, url_for

import config
import setup
from utils import user

app = Flask(__name__)

def validate_form(form, required_keys):
    return set(required_keys) <= set(form)

@app.route("/")
def index():
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
        if not validate_form(request.form, ["username", "password", "confirm_password", "zip_code"]):
            return render_template("register.html", message="Malformed request", category="danger")
        form = request.form
        username = form.get("username")
        password = form.get("password")
        password = form.get("password")
        confirm_password = form.get("confirm_password")
        zip_code = form.get("zip_code")
        if password != confirm_password:
            return render_template("register.html", message="Passwords do not match", category="danger")
        _user = user.get_user(username=username)
        if _user:
            return render_template("register.html", message="Username already in use.", category="danger")
        else:
            user.add_user(username, password, zip_code)
            return render_template("register.html", message="Account created", category="success")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.context_processor
def inject_username():
    """ Inject the username into each template, so we can render the navbar correctly. """
    if session.get("username"):
        return dict(username=session["username"])
    return dict()

if __name__ == "__main__":

    setup.initialize_tables()
    app.secret_key = config.SECRET_KEY
    app.config.from_object(config.options)

    app.debug = True
    app.run()
