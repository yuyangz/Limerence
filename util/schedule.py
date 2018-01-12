import time

# Constants
EMPTY = '(EMPTY)'
BREAKFAST = 'Breakfast'
LUNCH = 'Lunch'
DINNER = 'Dinner'
WORKOUT = 'Workout'
WORKOUT1 = 'preWorkout Session'
WORKOUT2 = 'Workout Session'
WORKOUT3 = 'postWorkout Session'


def get_music(time):
    # call from other class when completed.
    return ''  # default value for now


def clear_schedule(schedule, song_list, interval=None):
    # print(schedule)
    if interval is None:
        return new_schedule()
    num = int(interval)
    if 0 <= num <= 23:
        schedule[num], song_list[num] = EMPTY, EMPTY
    return schedule, song_list


def attempt_breakfast(schedule, song_list, breakfast_time):
    if breakfast_time > 11:
        print(BREAKFAST + ' is unavailable at this time.')
        return False
    if breakfast_time < 6:
        breakfast_time = 6
    schedule[breakfast_time], song_list[breakfast_time] = BREAKFAST, get_music(breakfast_time)
    return True


def attempt_lunch(schedule, song_list, start_time):
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
    schedule[lunch_time], song_list[lunch_time] = LUNCH, get_music(lunch_time)
    return True


def attempt_dinner(schedule, song_list, start_time):
    dinner_time = start_time
    for interval in range(start_time, 24):
        if schedule[interval][0] == LUNCH:
            dinner_time = interval + 5
            break
    if dinner_time > 22:
        print(DINNER + ' is unavailable at this time.')
        return False
    if dinner_time == start_time and dinner_time < 17:
        dinner_time = 17
    schedule[dinner_time], song_list[dinner_time] = DINNER, get_music(dinner_time)
    return True


def attempt_workout(schedule, song_list, start_time):
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
    schedule[workout_time], song_list[workout_time] = WORKOUT1, get_music(workout_time)
    schedule[workout_time + 1], song_list[workout_time + 1] = WORKOUT2, get_music(workout_time + 1)
    schedule[workout_time + 2], song_list[workout_time + 2] = WORKOUT3, get_music(workout_time + 2)
    return True


def new_schedule(curr_time=time.localtime()):
    print('It is currently {:02}:{:02}'.format(curr_time[3], curr_time[4]))
    schedule = [EMPTY] * 24  # military standard time
    song_list = [EMPTY] * 24  # military standard time
    start_hr = 5     # curr_time[3] + 1
    attempt_breakfast(schedule, song_list, start_hr)
    attempt_lunch(schedule, song_list, start_hr)
    attempt_dinner(schedule, song_list, start_hr)
    attempt_workout(schedule, song_list, start_hr)

    return schedule, song_list


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
