import requests, datetime

client_id= # INSERT CLIENT ID
client_secret= # INSERT CLIENT SECRET


# date = YYYYMMDD ('20170801')   place = `longitude, latitude` ('40.7243,-74.0018'), query = what you want ('coffee')
def get_area(date, place, query):
    params = dict(
        client_id=client_id,
        client_secret=client_secret,
        v=date,
        ll=place,
        query=query,
        limit=1
    )
    return requests.get(url='https://api.foursquare.com/v2/venues/explore', params=params).json()


def get_place(area_json):
    place = area_json['response']['groups'][0]['items'][0]['venue']
    print(place['name'])
    print(place['location']['formattedAddress'])


if __name__ == "__main__":
    data = get_area(datetime.datetime.today().strftime('%Y%m%d'), '40.7243,-74.0018', 'coffee')
    get_place(data)
