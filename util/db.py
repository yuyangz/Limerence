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

    #Add User Properties
    command1 = "INSERT INTO accounts VALUES(?, ?, ?, ?, ?, ?, ? ,? ,?, ?)"
    username = userinfo["username"]
    password = userinfo["password"]
    age = userinfo["age"]
    height = userinfo["height"]
    weight = userinfo["weight"]
    pfplink = userinfo["pfplink"]
    music = userinfo["music"]
    exercise = userinfo["excercise"]
    address = userinfo["address"]
    email = userinfo["email"]
    c.execute(command1, (username, password, age, height, weight, pfplink, music, exercise, address, email))

    #Create User Schedule Table
    command2 = "CREATE TABLE " + username + "(time TEXT, activity TEXT, music TEXT);"
    c.execute(command2)

    print "Created user schedule table\n"
    close(db)

'''userinfo = {"username": "anish2000", "password":"FOURWORDSALLLOWERCASE", "age": 56, "height": 250, "weight": 100, "pfplink": "http://google.com", "music": "rock", "excercise": "cardio", "address": "345 Chambers St", "email": "email@gmail.com"}
create_account(userinfo)'''

def check_account_exist(username):
    db = get_db()
    c = get_cursor(db)
    command = "SELECT username FROM accounts WHERE username = ?"
    usernames = c.execute(command, (username,))
    for list_username in usernames:
        return list_username != None
    close(db)
    return False

def check_account(username, password):
    db = get_db()
    c = get_cursor(db)
    if(check_account_exist(username)):
        command = "SELECT password FROM accounts WHERE username = ? "
        passdb = c.execute(command, (username, )).fetchone()
        close(db)
        return passdb[0] == password
    close(db)
    return False

'''
TODO:
    1) Function to get entire schedule
    2) Function to get Activity/Music based on a give time
    3) Function to reset schedule daily
'''


