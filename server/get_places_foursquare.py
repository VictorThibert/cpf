# get extra information from foursquare given restaurants from db

import os
import argparse
import json
import pprint
import requests
import sys
import urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode
from extensions import db

CLIENT_KEY = os.environ.get('FOURSQUARE_CLIENT_KEY')
SECRET_KEY = os.environ.get('FOURSQUARE_SECRET_KEY')


# api constants
API_HOST = 'https://api.foursquare.com/v2'
SEARCH_PATH = '/venues/search'
VENUE_PATH = '/venues/' 

SEARCH_LIMIT = 3
DEFAULT_RADIUS = 200 # in meters
DEFAULT_CATEGORIES = "restaurants"

def update_db(details, place_id): ## ERRR
    db.restaurants.update_one(
        {'place_id':place_id},
        {'$set':
            details
        },
            upsert=True
        )

def get_venue(api_key, venue_id):
    business_path = VENUE_PATH + venue_id
    return request(API_HOST, business_path, api_key)

def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()





def search(api_key, term, categories, coordinates, radius): ## ERR
    url_params = {
        'term': term.replace(' ', '+'),
        'latitude': coordinates['lat'],
        'longitude': coordinates['lng'],
        'radius': radius,
        'limit': SEARCH_LIMIT,
        'categories': categories,
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

def query_api(term, categories, coordinates, radius): ## ERRR
    response = search(API_KEY, term=term, categories=categories, coordinates=coordinates, radius=radius)
    businesses = response.get('businesses')
    if not businesses:
        print('No businesses for {0} in {1}, {2} found.'.format(term, coordinates['lat'], coordinates['lng']))
        return
    # recover first business in returned set
    business_id = businesses[0]['id']
    # get more information about specific business
    response = get_business(API_KEY, business_id)

    return response

def search_foursquare(place_name, location): ## ERR
    response = query_api(place_name, DEFAULT_CATEGORIES, location, DEFAULT_RADIUS)

    # only keep relevant details
    details = {}
    try:
        details['foursquare_review_count'] = response['review_count']
        details['foursquare_categories'] = response['categories']
        details['foursquare_id'] = response['id']
        details['foursquare_photos'] = response['photos']
        details['foursquare_rating'] = response['rating']
        details['foursquare_url'] = response['url']
        details['foursquare_location'] = response['location']
        details['foursquare_name'] = response['name']
    except (TypeError, KeyError) :
        details['foursquare_review_count'] = None
        details['foursquare_categories'] = []
        details['foursquare_id'] = None
        details['foursquare_photos'] = []
        details['foursquare_rating'] = None
        details['foursquare_url'] = None
        details['foursquare_location'] = None
        details['foursquare_name'] = None
    return details

# for each restaurant in db, query foursquare and update with additional information
def query_db():
    places = []
    cursor = db.restaurants.find()

    counter = 0
    for place in cursor:
        try:
            place_name = place['name']
            location = place['location']
            place_id = place['place_id']
        except KeyError:
            print('Key Error')
            continue

        print(counter, place_name, location)
        counter += 1
        details = search_foursquare(place_name, location)
        update_db(details, place_id)
    cursor.close()

def main():
    if (CLIENT_KEY is None) or (SECRET_KEY is None):
        print("provide client_key and secret_key")
        sys.exit(0)
    query_db()

if __name__ == '__main__':
    main()

