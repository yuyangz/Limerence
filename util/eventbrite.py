import urllib2
import keys
import json

APP_KEY = ""

def get_events(zipcode):
    global APP_KEY
    if APP_KEY == "":
        APP_KEY = keys.get_key("eventbrite")[0]
    events_url = "https://www.eventbriteapi.com/v3/events/search/?token=" + APP_KEY + "&location.address=<zipcode>&location.within=50mi"
    retList = []
    print events_url
    events = events_url.replace("<zipcode>", str(zipcode))
    response = urllib2.urlopen(events_url)
    url = response.geturl()
    info = response.read()
    info = json.loads(info)
    print info
    return info

if __name__ == '__main__':
    print get_events(11370)
