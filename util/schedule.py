from __future__ import print_function
import time
import spotify
import db
import weather

# Constants
EMPTY = '(EMPTY)'
BREAKFAST = 'Breakfast'
LUNCH = 'Lunch'
DINNER = 'Dinner'
WORKOUT = 'Workout'
WORKOUT1 = 'preWorkout Session'
WORKOUT2 = 'Workout Session'
WORKOUT3 = 'postWorkout Session'
SLEEP = "Sleep"
SHOWER = "Shower"


def get_music(time, username):
    # call from other class when completed.
    weather_to_scale = {"Rain": 0.5, "Drizzle": 0.9, "Thunderstorm": 0.25, "Snow": 0.75, "Atmosphere": 0.9, "Clear": 1.0, "Clouds":0.66, "Extreme":1.00, "Additional": 1.00}
    time_to_val = {0: 0.1, 1:0.1, 2:0.1, 3:0.1, 4:0.1, 5:0.1, 6:0.5, 7:0.5, 8:0.5, 9:0.5, 10:0.6, 11:0.7, 12:0.75, 13:0.8, 14:0.9, 15:1.0, 16:0.9, 17:0.7, 18:0.5, 19:0.4, 20:0.3, 21:0.25, 22:0.2, 23:0.2}
    genre = db.get_user_pref(username, "music")[0].lower()
    forecast = weather.get_weather(db.get_user_pref(username, "address")[0])['weather'][0]['main']
    val = time_to_val[time] * weather_to_scale[forecast]
    if (forecast == "Rain"):
        genre = "rainy-day"
        val = 0.5
    if (time > 22 or time < 5):
        genre = "sleep"
        val = 0.25
    print ("Time: " + str(time) + " Val: " + str(val))
    return spotify.get_song(genre, val)  # (genre, energy)


def clear_schedule(schedule, song_list, interval=None):
    # print(schedule)
    if interval is None:
        return new_schedule()
    num = int(interval)
    if 0 <= num <= 23:
        schedule[num], song_list[num] = EMPTY, EMPTY
    return schedule, song_list


def attempt_breakfast(schedule, song_list, breakfast_time, username):
    if breakfast_time > 11:
        print(BREAKFAST + ' is unavailable at this time.')
        return False
    if breakfast_time < 6:
        breakfast_time = 6
    schedule[breakfast_time], song_list[breakfast_time] = BREAKFAST, get_music(breakfast_time, username)
    return True


def attempt_lunch(schedule, song_list, start_time, username):
    lunch_time = start_time
    for interval in range(start_time, 24):
        if schedule[interval][0] == BREAKFAST:
            lunch_time = interval + 5
            break
    if lunch_time > 16:
        print(LUNCH + ' is unavailable at this time.')
        return False
    if lunch_time == start_time and lunch_time < 12:
        lunch_time = 12
    schedule[lunch_time], song_list[lunch_time] = LUNCH, get_music(lunch_time, username)
    return True


def attempt_dinner(schedule, song_list, start_time, username):
    dinner_time = start_time
    for interval in range(start_time, 24):
        if schedule[interval][0] == LUNCH:
            dinner_time = interval + 5
            break
    if dinner_time > 21:
        print(DINNER + ' is unavailable at this time.')
        return False
    if dinner_time == start_time and dinner_time < 17:
        dinner_time = 17
    schedule[dinner_time], song_list[dinner_time] = DINNER, get_music(dinner_time, username)
    return True


def attempt_workout(schedule, song_list, start_time, username):
    workout_time = -1
    skip = 0
    for interval in range(start_time, 22):
        skip -= 1
        if skip >= 0:
            continue
        if schedule[interval] == BREAKFAST or schedule[interval] == LUNCH or schedule[interval] == DINNER:
            skip = 2
        if schedule[interval] == EMPTY and schedule[interval + 1] == EMPTY and schedule[interval + 2] == EMPTY:
            workout_time = interval
            break

    if workout_time == -1:
        print(WORKOUT + ' is unavailable at this time.')
        return False
    schedule[workout_time], song_list[workout_time] = WORKOUT1, get_music(workout_time, username)
    schedule[workout_time + 1], song_list[workout_time + 1] = WORKOUT2, get_music(workout_time + 1, username)
    schedule[workout_time + 2], song_list[workout_time + 2] = WORKOUT3, get_music(workout_time + 2, username)
    return True


def place_shower(schedule, song_list, username):
    workout_time = -1
    breakfast_time = -1
    for interval in range(0, 22):
        if schedule[interval] == WORKOUT3:
            workout_time = interval
        if schedule[interval] == BREAKFAST:
            breakfast_time = interval

    shower_time = breakfast_time if workout_time == -1 else workout_time
    if shower_time == -1:
        shower_time = time.localtime()[3] + 1

    for interval in range(shower_time, 22):
        if schedule[interval] == EMPTY:
            schedule[interval], song_list[interval] = SHOWER, get_music(interval, username)
            break


def place_sleep(schedule, song_list, username):
    schedule[10], song_list[10] = SLEEP, get_music(10, username)


def new_schedule(username, curr_time=time.localtime()):
    print('It is currently {:02}:{:02}'.format(curr_time[3], curr_time[4]))
    schedule = [EMPTY] * 24  # military standard time
    song_list = [EMPTY] * 24  # military standard time
    start_hr = curr_time[3]    # curr_time[3] + 1
    print (start_hr)
    attempt_breakfast(schedule, song_list, start_hr, username)
    attempt_lunch(schedule, song_list, start_hr, username)
    attempt_dinner(schedule, song_list, start_hr, username)
    attempt_workout(schedule, song_list, start_hr, username)
    place_shower(schedule, song_list, username)
    place_sleep(schedule, song_list, username)
    fin_sched = {}
    for i in range(start_hr, 24):
        if song_list[i] == EMPTY:
            song_list[i] = get_music(i, username)
        fin_sched[i] = {"activity":schedule[i], "music":song_list[i]}
    print (fin_sched)
    return fin_sched


def print_schedule(schedule, song_list):
    print(len(schedule))
    if len(schedule) == 0:
        print("Input parameters are currently Empty")
        return
    for interval in range(0, 24):
        print('{:02} - {} + {}'.format(interval, schedule[interval], song_list[interval]))


if __name__ == '__main__':
    (schedule, song_list) = new_schedule()
    # print_schedule(schedule, song_list)
    clear_schedule(schedule, song_list, interval=3)
    print_schedule(schedule, song_list)
