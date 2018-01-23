from flask import Flask, render_template, request, session, redirect, flash, url_for
from util import db
from datetime import datetime
import time
from util import schedule
from time import localtime
import os, cgi, hashlib, sys

if sys.platform != 'win32':			# Windows does not support SIGPIPE
	from signal import signal, SIGPIPE, SIG_DFL
	signal(SIGPIPE, SIG_DFL)


app = Flask(__name__)
app.secret_key = os.urandom(32)

global g_schedule
global g_song_lists


@app.route("/scheduler")
def scheduler():
	if "username" not in session.keys():
		return redirect(url_for("login"))
	global g_schedule
	global g_song_lists

	username = session["username"]
	
	curr_time = int(time.time())  # epoch time
	last_accessed = db.get_user_pref(username, "last_accessed")[0]

	# If we have already accessed the schedule today
	if datetime.fromtimestamp(curr_time).date() == datetime.fromtimestamp(last_accessed).date():
		if g_schedule is not None and g_song_lists is not None:
			return render_template("schedule.html", name=username, sch=g_schedule, \
				song=g_song_lists, clock=range(localtime()[3], 24))
		
		# else not stored in memory -> must retrieve from database
		combinded_sch = db.get_schedule(username)

		g_song_lists = [schedule.EMPTY] * 24
		g_schedule = [schedule.EMPTY] * 24
		for i in range(24):
			g_schedule[i] = combinded_sch[i]["activity"]
			g_song_lists[i] = combinded_sch[i]["music"]

	else:
		sch = schedule.new_schedule(username)
		g_schedule = sch[0]
		g_song_lists = sch[1]

		combinded_sch = [schedule.EMPTY] * 24
		for i in range(24):
			combinded_sch[i] = {"activity": g_schedule[i], "music": g_song_lists[i]}

		db.reset_sched(username, combinded_sch)
		db.edit_user_pref(username, "last_accessed", curr_time)
	return render_template("schedule.html", name=username, sch=g_schedule, song=g_song_lists,\
		clock=range(localtime()[3], 24))


@app.route("/rmSchedule")
def rm_schedule():
	if "username" not in session.keys():
		return redirect(url_for("login"))
	global g_schedule
	global g_song_lists

	id = request.args["id"]
	g_schedule, g_song_lists = schedule.clear_schedule(g_schedule, g_song_lists, session["username"], interval=id)
	return render_template("schedule.html", name=session["username"], sch=g_schedule, song=g_song_lists,
						   clock=range(localtime()[3], 24))


@app.route("/recommendations")
def recommendations():
	if "username" not in session.keys():
		return redirect(url_for("login"))
	global g_schedule
	global g_song_lists

	if g_schedule == None:
		flash("Check out your schedule first!")
		return redirect(url_for("scheduler"))

	events = schedule.random_events
	return render_template("recommendations.html", name=session["username"], sch=events, \
		num_events=range(len(events)), clock = range(localtime()[3], 22))


@app.route("/recommended")
def recommended_spot():
	if "username" not in session.keys():
		return redirect(url_for("login"))
	global g_schedule
	global g_song_lists

	print(request.args["time_hr"], request.args["event"])
	g_schedule[int(request.args["time_hr"])] = request.args["event"]
	return redirect(url_for("scheduler"))


@app.route("/")
def hello_world():
	'''
	If session has a record of the correct username and password input, the user is logged in
	Otherwise, the login page is displayed
	'''
	if "username" in session.keys():
		return render_template("schedule.html", name=session["username"])
	return render_template("home.html")


@app.route("/createaccount")
def display_signup():
	if "username" in session.keys():
		return render_template("schedule.html", name=session["username"])
	return render_template("createaccount.html")


@app.route("/signup")
def create_account():
	if "username" in session.keys():
		return redirect(url_for("welcome"))
	user = request.args["username"]
	if request.args["pwd1"] == request.args["pwd2"]:
		if db.check_account_exist(user):
			flash("Username is already taken")
			return redirect(url_for("display_signup"))
		db.create_account(request.args)
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
	flash("Credentials invalid")
	return redirect(url_for("display_login"))


@app.route("/profile")
def logged_in():
	if "username" not in session.keys():
		return redirect(url_for("login"))
	return render_template("profile.html", name=session["username"],
						   info=db.get_all_user_preferences(session["username"]))


@app.route("/edit_profile")
def edit_profile():
	if "username" not in session.keys():
		return redirect(url_for("login"))
	return render_template("edit_profile.html", name=session["username"],
						   info=db.get_all_user_preferences(session["username"]))


@app.route("/update_profile")
def update_profile():
	if "username" not in request.args:
		flash("Not logged in")
		return redirect(url_for("display_login"))
	user = request.args["username"]

	# "age", "height", "weight", "pfplink", "music", "excercise", "address", "email"
	db.edit_user_pref(user, "age", request.args['age'])
	db.edit_user_pref(user, "height", request.args['height'])
	db.edit_user_pref(user, "weight", request.args['weight'])
	db.edit_user_pref(user, "pfplink", request.args['pfplink'])
	db.edit_user_pref(user, "music", request.args['music'])
	db.edit_user_pref(user, "excercise", request.args['excercise'])
	db.edit_user_pref(user, "address", request.args['address'])
	db.edit_user_pref(user, "email", request.args['email'])

	flash("Profile successfully updated")
	return redirect(url_for("logged_in"))


@app.route("/login")
def display_login():
	return render_template("login.html")


@app.route("/logout")
def logged_out():
	if "username" not in session.keys():
		return redirect(url_for("hello_world"))
	session.clear()  # Ends session
	return redirect("/")  # Redirecting to login

@app.route("/userhome")
def user_home():
        return render_template("user_home.html")


if __name__ == "__main__":
	g_schedule = None
	g_song_lists = None
	app.debug = True
	app.run()
