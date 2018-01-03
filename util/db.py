import sqlite3
from os.path import isfile
import hashlib

path = "data/data.db"

def get_db(): #returns connection to database
	return sqlite3.connect(path)

def get_cursor(db): #returns cursor to database
	return db.cursor()

def close(db): #commits to and closes database
	db.commit()
	db.close()
	
#============================================================#
#============================Users=========================#
#============================================================#

'''
	takes in dictionary of:
		username
		password
		age
		height
		weight
		pfplink
		music
		excercise
		address
		email
'''

def create_account(userinfo):
	print "Creating Account...\n"
	db = get_db()
	c = get_cursor(db)
	command = "INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?, ? ,? ,?, ?)"
	username = userinfo["username"]
	password = userinfo["password"]
	age = userinfo["age"]
	height = userinfo["height"]
	weight = userinfo["weight"]
	pfplink = userinfo["pfplink"]
	music = userinfo["music"]
	excercise = userinfo["excercise"]
	address = userinfo["address"]
	email = userinfo["email"]
	c.execute(command, (username, password, age, height, weight, pfplink, music, excercise, address, email))
	close(db)

'''userinfo = {"username": "anish2000", "password":"FOURWORDSALLLOWERCASE", "age": 56, "height": 250, "weight": 100, "pfplink": "http://google.com", "music": "rock", "excercise": "cardio", "address": "345 Chambers St", "email": "email@gmail.com"}
create_account(userinfo)'''

def 


	
