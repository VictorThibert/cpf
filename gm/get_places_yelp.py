# get extra information from yelp given restaurants from db

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
import geopy.distance
from fuzzywuzzy import fuzz

API_KEY = os.environ.get('YELP_API_KEY')


# api constants
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/' 

SEARCH_LIMIT = 3
DEFAULT_RADIUS = 200 # in meters
DEFAULT_CATEGORIES = "restaurants"
MAXIMUM_DISTANCE = 50 # in meters for locations to even be considered the same
MINIMUM_WORDSCORE = 60

def update_db(details, place_id):

    db.restaurants.update_one(
        {'place_id':place_id},
        {'$set':
            details
        },
            upsert=True
    )

def get_business(api_key, business_id):
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)

def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

def search(api_key, term, categories, coordinates, radius):
    url_params = {
        'term': term.replace(' ', '+'),
        'latitude': coordinates['lat'],
        'longitude': coordinates['lng'],
        'radius': radius,
        'limit': SEARCH_LIMIT,
        'categories': categories,
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


# looks for yelp restaurant based on google place name
def query_api(term, categories, coordinates, radius):
    response = search(API_KEY, term=term, categories=categories, coordinates=coordinates, radius=radius)
    businesses = response.get('businesses')

    if not businesses:
        # print('NO {0} at {1}, {2}'.format(term, round(coordinates['lat'],2), round(coordinates['lng'],2)))
        return

    # recover first business in returned set
    business_id = businesses[0]['id']

    # get more information about specific business
    response = get_business(API_KEY, business_id)

    return response

def get_wordscore(word_1, word_2):
    word_1 = word_1.replace('restaurant','')
    word_1 = word_1.replace('Restaurant','')
    word_2 = word_2.replace('restaurant','')
    word_2 = word_2.replace('Restaurant','')
    score = fuzz.token_sort_ratio(word_1, word_2)
    return score


# verify if returned restaurant is similar enough 
def validate_match(google_name, coordinates, tentative_name, tenatative_coordinates):
    is_similar = False

    c1 = (coordinates['lat'], coordinates['lng'])
    c2 = (tenatative_coordinates['latitude'], tenatative_coordinates['longitude'])

    distance = 0

    try: 
        distance = geopy.distance.vincenty(c1, c2).m
    except ValueError:
        return False

    if (distance <= MAXIMUM_DISTANCE) and (get_wordscore(google_name, tentative_name) >= MINIMUM_WORDSCORE): # check word similarity and distance 
        is_similar = True

    if is_similar:
        print(google_name, " IS ", tentative_name)
    else:
        print(google_name, " NOT ", tentative_name)
    return is_similar


def search_yelp(google_name, coordinates):
    response = query_api(google_name, DEFAULT_CATEGORIES, coordinates, DEFAULT_RADIUS)

    is_valid = False
    tentative_name = ''
    tenatative_coordinates = {}

    # only keep relevant details
    details = {}
    details['yelp_review_count'] = None
    details['yelp_categories'] = None
    details['yelp_id'] = None
    details['yelp_photos'] = None
    details['yelp_rating'] = None
    details['yelp_url'] = None
    details['yelp_location'] = None
    details['yelp_name'] = None
    details['yelp_price'] = None

    try: 
        tentative_name = response.get('name', None)
        tenatative_coordinates = response.get('coordinates', {'latitude': None, 'longitude':None})
    except AttributeError:
        return details 

    is_valid = validate_match(google_name, coordinates, tentative_name, tenatative_coordinates) 

    if is_valid:
        details['yelp_review_count'] = response.get('review_count', None)
        details['yelp_categories'] = response.get('categories',[])
        details['yelp_id'] = response.get('id', None)
        details['yelp_photos'] = response.get('photos',[])
        details['yelp_rating'] = response.get('rating', 0.0)
        details['yelp_url'] = response.get('url', None)
        details['yelp_location'] = response.get('location', None)
        details['yelp_name'] = response.get('name', None)
        details['yelp_price'] = response.get('price', None)

    return details

# for each restaurant in db, query yelp and update with additional information
def query_db():
    for place in db.restaurants.find():
        try:
            place_name = place['name']
            coordinates = place['location']
            place_id = place['place_id']
        except KeyError:
            print('Key Error')

        #print(place_name, coordinates)

        # location is in {lat:, lng}
        details = search_yelp(place_name, coordinates)

        update_db(details, place_id)

def main():
    if API_KEY is None:
        print("No API_KEY provided")
        sys.exit(0)
    query_db()

if __name__ == '__main__':
    main()

