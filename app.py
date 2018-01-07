from flask import Flask, render_template, request, session, redirect, flash, url_for
#from util import db
from util import db
from datetime import datetime

import os, cgi, hashlib

app = Flask (__name__)

#the_username = "user" #Hardcoded username
#the_password = "pwd"  #Hardcoded password
app.secret_key = os.urandom(32)

global username

def get_username():
    global username
    return username


@app.route("/")
def hello_world():
    '''
    If session has a record of the correct username and password input, the user is logged in
    Otherwise, the login page is displayed
    '''
    if "username" in session.keys():
        return render_template("welcome.html", name = session["username"])
    return render_template("login.html", message = "")

@app.route("/createaccount")
def create_account():
    return render_template("createaccount.html")

@app.route("/auth")
def check_creation():
    user = request.args["username"]
    #if request.args["username"] is unique will do later
    if request.args["password1"] == request.args["password2"]:
        pwd = request.args["password1"]
        unique = db.create_account(userinfo)
        if unique:
            flash("Success!")
            return redirect(url_for("hello_world"))
        else:
            flash ("Oops this user already exists")
            return redirect(url_for("create_account"))
    else:
        flash("Passwords do not match :(")
        return redirect(url_for("create_account"))


@app.route("/welcome")
def logged_in():
   input_name = request.args["username"]
   input_pass = request.args["password"]
   hash_object = hashlib.sha224(input_pass)
   hashed_pass = hash_object.hexdigest()
   #Validation process, what went wrong (if anything)?
   if lookup[0]:
        if hashed_pass == lookup[1][0]:
            session["username"] = input_name #Creates a new session
            global username
            username = input_name
            return render_template("welcome.html", name = input_name)
        else:
            return render_template("login.html", message = "Error: Wrong password")
   else:
        return render_template("login.html", message =  "Error: Wrong username")

@app.route("/logout")
def logged_out():
    if not "username" in session.keys():
        return redirect(url_for("hello_world"))
    session.pop("username") #Ends session
    return redirect("/") #Redirecting to login

if __name__ == "__main__":
    app.debug = True
    app.run()
