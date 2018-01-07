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
    try:
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
    except:
        return ""
    c.execute(command1, (username, password, age, height, weight, pfplink, music, exercise, address, email))

    #Create User Schedule Table
    command2 = "CREATE TABLE " + username + "(time INT PRIMARY KEY, activity TEXT, music TEXT);"
    c.execute(command2)

    print "Created user schedule table\n"
    close(db)


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

#============================================================#
#============================Schedules=========================#
#============================================================#

'''
Returns the entire schedule of user as a dictionary
format: {time: {activity: "activity", music: "music"}, time: {activity: "activity", music: "music"}, ...}
'''
def get_schedule(username):
    db = get_db()
    c = get_cursor(db)
    if(check_account_exist(username)):
        command = "SELECT * FROM " + username + ";"
        sched = c.execute(command).fetchall()
        close(db)
        d = {}
        for line in sched:
            d[line[0]] = {"activity": line[1], "music": line[2]}
        return d
    else:
        print "Username not found - Could not get schedule"
        close(db)

'''
Takes in Dict in format:
  {time: {"activity": "ex_activity", "music": "ex_song"], time: {"activity": "ex_activity2", "music": "ex_song2"], ...}
  "time" is a single int representing the start time (each hour has a section in the table)
  ex: if time = 4 then the activities corresponding to that time go on from 4am-5am
'''
def reset_sched(username, sched_dict):
    db = get_db()
    c = get_cursor(db)
    if(check_account_exist(username)):
        for time in sched_dict:
            activity = sched_dict[time]["activity"]
            song = sched_dict[time]["music"]
            print("Inserting: ")
            print("Time: " + str(time))
            print("Activity: " + activity)
            print("Song: " + song)
            command = "INSERT INTO " + username + "(time, activity, music) VALUES(?, ?, ?);"
            c.execute(command, (time, activity, song))
    else:
        print "Username Not Found - Cannot Reset Schedule"
    close(db)

'''
Takes in a username and time of day
input time is in format of '2011-05-03 17:45:35.177000' (use str(datetime.now()))
Returns dict of format {"activity": "ex_activity", "music": "ex_song"}
'''
def get_activ_music(username, time):
    hour = int(time[11:13])
    sched = get_schedule(username)
    if(sched != None and hour in sched):
        print ("Time: " + str(hour))
        print ("Activity: ")
        print sched[hour]
        return sched[hour]
    print "No Schedule Found"

'''
TESTS:
userinfo = {"username": "anish2000", "password":"FOURWORDSALLLOWERCASE", "age": 56, "height": 250, "weight": 100, "pfplink": "http://google.com", "music": "rock", "excercise": "cardio", "address": "345 Chambers St", "email": "email@gmail.com"}
create_account(userinfo)
sched = {12: {"activity": "Canned Sardines", "music":"Hey Jude"}, 13:{"activity": "Swimming", "music": "Moon"}}
reset_sched("anish2000", sched)
print(get_schedule("anish2000"))
get_activ_music("anish2000", "2011-05-03 12:45:35.177000")
get_activ_music("anish2000", "2014-23-03 13:45:35.177000")
get_activ_music("anish2000", "2033-05-05 14:45:35.177000")
'''
