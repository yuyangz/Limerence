from __future__ import print_function
import requests, time
from . import keys

global weather
global last_city
global last_time
global WEATHER_KEY

WEATHER_KEY = "" # Input API Key

weather = None
last_city = None    # if you call too many times, it locks you out for one hour...
last_time = None


# populates global weather with json from api
# designed for internal use
def get_raw_weather(city):
    global weather
    global last_city
    global last_time
    global WEATHER_KEY

    if city == last_city and last_time - time.time() < 60: # 60 sec
        print('last_city triggered by ' + city)
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


def get_time(unix_time, GMT):
    time = unix_time % (60 * 60 * 24)
    seconds = time % (24 * 60) % 60
    minutes = time % (24 * 60) / 60
    hours = time / (60 * 60)
    return '{}:{}:{}'.format(hours + GMT, minutes, seconds)


def get_forecast(city):
    """ returns a tuple of (description, temperature, humidity, sunrise, sunset)"""
    global WEATHER_KEY
    if WEATHER_KEY == "":
        WEATHER_KEY = keys.get_key("openweathermap")[0]

    weather = get_raw_weather(city)
    if 'message' in weather:        # inputed invalid city
        print(weather['message'])
        return 'Extreme', -100, 100, "00:00:00", "00:00:00"

    # prints description (e.g. cloudy, rain)
    print("description", weather['weather'][0]['main'])
    # prints temperature (converted to Farenheit from Kelvin)
    print("temperature", weather['main']['temp'] * 9 / 5 - 459.67)
    # prints humidity
    print("humidity", weather['main']['humidity'])
    # sunrise and sunset from midnight
    print("sunrise", get_time(weather['sys']['sunrise'], GMT('NY')))
    print("sunset", get_time(weather['sys']['sunset'], GMT('NY')))
    return weather['weather'][0]['main'], weather['main']['temp'] * 9 / 5 - 459.67, \
            weather['main']['humidity'], get_time(weather['sys']['sunrise'], GMT('NY')),\
            get_time(weather['sys']['sunset'], GMT('NY'))


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
