# get extra information from foursquare given restaurants from db

import os
import argparse
import json
import pprint
import requests
import sys
from bson.objectid import ObjectId
import urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode
from extensions import db
import pprint

CLIENT_KEY = os.environ.get('FOURSQUARE_CLIENT_KEY')
SECRET_KEY = os.environ.get('FOURSQUARE_SECRET_KEY')


# api constants
API_HOST = 'https://api.foursquare.com/v2'
SEARCH_PATH = '/venues/search'
VENUE_PATH = '/venues/'
VERSION = 20180102 ## YYYMMDD of the version we want to sue

SEARCH_LIMIT = 3
DEFAULT_RADIUS = 200 # in meters
DEFAULT_CATEGORIES = "restaurants"

def update_db(details, _id):
    db.restaurants.update_one(
        {'_id': ObjectId(_id) },
        {'$set':
            details
        },
            upsert=True
        )

def search_foursquare(place_name, location):
    response = query_api(place_name, location)
    response = response['response']['venue']
    # only keep relevant details
    details = {}
    details['id'] = response['id']
    details['likes'] = response['likes']
    if(details['likes'] != False): details['likes'] = response['likes']['count']
    else: details['likes'] = 0

    if(response['dislike'] != False): details['dislike'] = response['dislike']['count']
    else: details['dislike'] = 0

    if(response['ok'] != False): response['ok'] = response['ok']['count']
    else: details['ok'] = 0
    return details


def get_venue(venue_id):
    venue_path = VENUE_PATH + venue_id
    params = {
        'client_id':CLIENT_KEY,
	'client_secret':SECRET_KEY,
	'v':VERSION
    }
    return request(API_HOST, venue_path, url_params=params)

def request(host, path, url_params={}):
    url = '{0}{1}'.format(host, path)
    #print("going to get from the url: ", url)
    response = requests.request('GET', url, params=url_params)
    return response.json()

def search(name, location):
    ll = str(location['lat'])+','+str(location['lng'])
    url_params = {
        'client_id':CLIENT_KEY,
	'client_secret':SECRET_KEY,
	'v':VERSION,
	'match':'intent',
        'name': name,
        'll':ll
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def query_api(name, location):
    response = search(name, location)
    results = response['response']['venues']
    if len(results) == 0:
        print('No venue for {0} in {1}, {2} found.'.format(name, location['lat'], location['lng']))
        return
    venue_id = results[0]['id']
    response = get_venue(venue_id)
    return response

# def my_print(obj):
#   for a in obj.keys():
#     print("key: ", a , " type: ", type(obj[a]))
#     if(type(obj[a]) != str): print(a,"=",obj[a])
#     else: print(a,"=", obj[a].encode('utf8'))

# for each restaurant in db, query foursquare and update with additional information
def query_db():
    places = []
    cursor = db.restaurants.find()

    counter = 0
    for place in cursor:
        _id = place['_id']
        print("_id: ", _id)
        #place_utf = {k: (place[k]).encode("utf-8") for k in place.keys()}
        #try:
        place_name = place.get('name', None)
        print("place_name: ", place_name.encode('utf-8'))
        location = place.get('location', None)
        print("location: ", location)
        if(location == None or place_name == None): continue
        place_name = place_name.encode('utf-8')

        print(counter, place_name, location)
        counter += 1
        details = search_foursquare(place_name, location)
        update_db(details, _id)
    cursor.close()

def main():
    if (CLIENT_KEY is None) or (SECRET_KEY is None):
        print("provide client_key and secret_key")
        sys.exit(0)
    query_db()

if __name__ == '__main__':
    main()

