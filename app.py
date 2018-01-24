from flask import Flask, render_template, request, session, redirect, flash, url_for
from util import db
from datetime import datetime
import time
from util import schedule
from time import localtime
from util import eventbrite
import os, cgi, hashlib, sys

if sys.platform != 'win32':			# Windows does not support SIGPIPE
	from signal import signal, SIGPIPE, SIG_DFL
	signal(SIGPIPE, SIG_DFL)


app = Flask(__name__)
app.secret_key = os.urandom(32)

global g_schedule
global g_song_lists
g_food_rec = {}
g_events = []


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
            return render_template("schedule.html", name=username.title(), sch=g_schedule, \
				song=g_song_lists, clock=range(localtime()[3], 24))

		# else not stored in memory -> must retrieve from database
        combined_sch = db.get_schedule(username)

        g_song_lists = [schedule.EMPTY] * 24
        g_schedule = [schedule.EMPTY] * 24
        for i in range(24):
			g_schedule[i] = combined_sch[i]["activity"]
			g_song_lists[i] = combined_sch[i]["music"]
    else:
        sch = schedule.new_schedule(username)
        g_schedule = sch[0]
        g_song_lists = sch[1]

        combined_sch = [schedule.EMPTY] * 24
        for i in range(24):
			combined_sch[i] = {"activity": g_schedule[i], "music": g_song_lists[i]}

        db.reset_sched(username, combined_sch)
        db.edit_user_pref(username, "last_accessed", curr_time)
    return render_template("schedule.html", name=username.title(), sch=g_schedule, song=g_song_lists, clock=range(localtime()[3], 24))

@app.route("/rmSchedule")
def rm_schedule():
	if "username" not in session.keys():
		return redirect(url_for("login"))
	global g_schedule
	global g_song_lists

	id = request.args["id"]
	g_schedule, g_song_lists = schedule.clear_schedule(g_schedule, g_song_lists, session["username"], interval=id)
	return render_template("schedule.html", name=session["username"].title(), sch=g_schedule, song=g_song_lists, clock=range(localtime()[3], 24))

@app.route("/recommendations")
@app.route("/recommendations/<pref>/<new_val>")
@app.route("/recommendations/<pref>/<new_val>/<is_event>")
def recommendations(pref=None, new_val=None, is_event="False"):
    if "username" not in session.keys():
        return redirect(url_for("login"))
    username = session["username"]
    if pref != None and new_val != None:
        cats = ["music", "activity"]
        if pref not in cats:
            print "CANNOT CHANGE SCHED"
            return redirect(url_for("recommendations"))
        new_time = int(request.args["time_hr"])
        curr = db.get_activ_music(username, int(new_time))
        for cat in cats:
            if pref == cat:
                if is_event == "True":
                    if int(new_val) <= len(g_events):
                        new_val = g_events[int(new_val)]
                    else:
                        print "CANNOT EDIT SCHED"
                curr[pref] = new_val
                break
        db.edit_sched(username, new_time, curr)
        if g_schedule is not None and g_song_lists is not None:
            g_schedule[new_time] = curr["activity"]
            g_song_lists[new_time] = curr["music"]
        return redirect(url_for("scheduler"))
    rec_songs = schedule.get_music(time.localtime()[3], username, False)
    sch = [] #List Of Activities
    exercises = []
    for i in range(7):
        exercises.append(schedule.get_workout())
    zipcode = db.get_user_pref(username, "address")
    events = eventbrite.get_events(zipcode)["events"][:5]
    global g_events
    for event in events:
        text = (event["description"]["text"] + " <br><a href='" + event["url"] + "'>LINK</a>")
        sch.append(text)
        g_events.append(text)
    foods = {}
	#If Breakfast time
    if(time.localtime()[3] < 7):
		path = "./static/breakfast.txt"
    else:
		path = "./static/lunchdinner.txt"
    for i in range(10):
        #print i
        food_data = schedule.get_food(path)
        foods[food_data[0]] = food_data[1]
        exercises.append(schedule.get_workout())
    clock = range(localtime()[3], 22)
    global g_food_rec
    g_food_rec = foods
    #print len(clock)
    #print (exercises)
    if len(clock) == 0:
		clock = 0
    return render_template("recommendations.html", name=username.title(), sch=sch, exercises = exercises, songs=rec_songs, clock = clock, foods=foods)


@app.route("/")
def hello_world():
    '''
	If session has a record of the correct username and password input, the user is logged in
	Otherwise, the login page is displayed
	'''
    if "username" in session.keys():
		return render_template("schedule.html", name=session["username"].title())
    return render_template("home.html")


@app.route("/createaccount")
def display_signup():
	if "username" in session.keys():
		return render_template("schedule.html", name=session["username"].title())
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
		return redirect(url_for("user_home"))
	flash("Credentials invalid")
	return redirect(url_for("display_login"))


@app.route("/profile")
def logged_in():
	if "username" not in session.keys():
		return redirect(url_for("login"))
	return render_template("profile.html", name=session["username"].title(),
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
    db.edit_all_user_pref(user, request.args)
    db.edit_user_pref(user, "last_accessed", 0)

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

@app.route("/fooddescription/<name>")
def food_description(name):
    if name not in g_food_rec.keys():
        print "FOOD INFO UNAVAILABLE"
        return redirect(url_for("recommendations"))
    food = g_food_rec[name]
    return render_template("food_descriptions.html", food = food, name=name)


if __name__ == "__main__":
	g_schedule = None
	g_song_lists = None
	app.debug = True
	app.run()
