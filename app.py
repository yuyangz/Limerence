from flask import Flask, render_template, request, session, redirect, flash, url_for
#from util import db
from util import db
from datetime import datetime
from util import schedule
from time import localtime

import os, cgi, hashlib

app = Flask (__name__)

app.secret_key = os.urandom(32)

global g_schedule
global g_song_lists

@app.route("/scheduler")
def scheduler():
    global g_schedule
    global g_song_lists

    sch = schedule.new_schedule()
    g_schedule = sch[0]
    g_song_lists = sch[1]
    return render_template("schedule.html", name="User", sch=g_schedule, song=g_song_lists, clock=range(localtime()[3], 24))


@app.route("/rmSchedule")
def rm_schedule():
    global g_schedule
    global g_song_lists

    id = request.args["id"]
    g_schedule, g_song_lists = schedule.clear_schedule(g_schedule, g_song_lists, interval=id)
    return render_template("schedule.html", name="User", sch=g_schedule, song=g_song_lists, clock=range(localtime()[3], 24))

@app.route("/recommendations")
def recommendations():
    global g_schedule
    global g_song_lists

    sch = schedule.new_schedule()
    g_schedule = sch[0]
    g_song_lists = sch[1]
    return render_template("recommendations.html", name="User", sch=g_schedule, song=g_song_lists, clock=range(localtime()[3], 24))

@app.route("/")
def hello_world():
    '''
    If session has a record of the correct username and password input, the user is logged in
    Otherwise, the login page is displayed
    '''
    if "username" in session.keys():
        return render_template("welcome.html", name = session["username"])
    return render_template("home.html")

@app.route("/createaccount")
def display_signup():
    if "username" in session.keys():
        return render_template("welcome.html", name = session["username"])
    return render_template("createaccount.html")

@app.route("/signup")
def create_account():
    if "username" in session.keys():
        return redirect(url_for("welcome"))
    user = request.args["username"]
    if request.args["pwd1"] == request.args["pwd2"]:
        if db.check_account_exist(user):
            flash("User already exists")
            return redirect(url_for("display_signup"))
        db.create_account(request.args);
        flash("User created")
        return redirect(url_for("display_login"))
    else:
        flash("Passwords do not match :(")
        return redirect(url_for("display_signup"))

@app.route("/auth")
def login():
    if "username" not in request.args:
        flash("Not logged in")
        return redirect(url_for("display_login"))
    auth = db.check_account(request.args["username"], request.args["pwd"])
    if auth:
        session["username"] = request.args["username"]
        flash("Logged in!")
        return redirect(url_for("logged_in"))
    flash("Credentials invalid");
    return redirect(url_for("display_login"))

@app.route("/welcome")
def logged_in():
    pass
    if "username" not in session.keys():
        return redirect(url_for("login"))
    return render_template("welcome.html")


@app.route("/login")
def display_login():
    return render_template("login.html")


@app.route("/logout")
def logged_out():
    if not "username" in session.keys():
        return redirect(url_for("hello_world"))
    session.pop("username") #Ends session
    return redirect("/") #Redirecting to login


if __name__ == "__main__":
    app.debug = True
    app.run()
