from __future__ import print_function
import requests, time
import keys

WEATHER_KEY = "" # Input API Key

weather = None
last_city = None    # if you call too many times, it locks you out for one hour...
last_time = None


# populates global weather with json from api
def get_weather(city):
    global weather
    global last_city
    global last_time
    global WEATHER_KEY
    if WEATHER_KEY == "":
        WEATHER_KEY = keys.get_key("openweathermap")[0]

    if city == last_city and last_time - time.time() < 60: # 60 sec
        return weather

    last_city = city
    last_time = time.time()
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + WEATHER_KEY
    # print url
    weather = requests.get(url).json()
    return weather


def GMT(place):
    if place == 'NY':
        return -5


def print_time(unix_time, GMT):
    time = unix_time % (60 * 60 * 24)
    seconds = time % (24 * 60) % 60
    minutes = time % (24 * 60) / 60
    hours = time / (60 * 60)
    # print hours, ":", minutes, ":", seconds, " GMT"
    print('{}:{}:{}'.format(hours + GMT, minutes, seconds))
    # print hours + GMT, minutes, seconds


def get_forecast(city):
    global WEATHER_KEY
    if WEATHER_KEY == "":
        WEATHER_KEY = keys.get_key("openweathermap")[0]

    weather = get_weather(city)
    # prints description (e.g. cloudy, rain)
    print(weather['weather'][0]['main'])
    # prints temperature (converted to Farenheit from Kelvin)
    print(weather['main']['temp'] * 9 / 5 - 459.67)
    # prints humidity
    print(weather['main']['humidity'])
    # sunrise and sunset from midnight
    print_time(weather['sys']['sunrise'], GMT('NY'))
    print_time(weather['sys']['sunset'], GMT('NY'))
    return weather['weather'][0]['main']


if __name__ == '__main__':
    global weather
    global last_city
    global last_time

    weather = None
    last_city = None
    last_time = time.time()

    get_forecast('Boston')
    get_forecast('Brooklyn')
    # print_time(1515413584, GMT('NY'))
