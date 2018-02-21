# get restaurant data from yelp and pair with current db

import argparse
import geopy.distance
import json
import os
import pprint
import requests
import sys
import urllib
import time

from extensions import db
from fuzzywuzzy import fuzz
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

API_KEY = os.environ.get('YELP_API_KEY')

# api constants
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/' 

# search constants
SEARCH_LIMIT = 3
DEFAULT_RADIUS = 200 # in meters
DEFAULT_CATEGORIES = "restaurants"
MAXIMUM_DISTANCE = 75 # in meters for locations to even be considered the same
MINIMUM_WORDSCORE = 60

# insert the updated document into mongo, based on google place_id
def update_db(details, place_id):
    db.restaurants.update_one(
        {'place_id':place_id},
        {'$set':
            details
        },
        upsert=True
    )

# create yelp api request
def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    # temporary
    respose = {}
    try:
        response = requests.request('GET', url, headers=headers, params=url_params)
    except ConnectionError as e:
        print('Request Error (Sleep 5 seconds)')
        time.sleep(5)
        try:
            response = requests.request('GET', url, headers=headers, params=url_params)
        except ConnectionError as f:
            print('2nd request error: skip')

    return response.json()

# send a yelp api call to get more details about a particular yelp_business
def get_business_details(api_key, business_id):
    business_path = BUSINESS_PATH + business_id
    return request(API_HOST, business_path, api_key)

# search yelp for restaurants in general vicinity with proper name
def get_yelp_search_results(api_key, term, categories, coordinates, radius):
    url_params = {
        'term': term.replace(' ', '+'),
        'latitude': coordinates['lat'],
        'longitude': coordinates['lng'],
        'radius': radius,
        'limit': SEARCH_LIMIT,
        'categories': categories,
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


# look for yelp restaurant based on google place name
def get_yelp_restaurants(term, categories, coordinates, radius):
    response = get_yelp_search_results(API_KEY, term=term, categories=categories, coordinates=coordinates, radius=radius)
    businesses = response.get('businesses')

    # no businesses found
    if not businesses:
        # print('NO {0} at {1}, {2}'.format(term, round(coordinates['lat'],2), round(coordinates['lng'],2)))
        return

    # recover first business in returned set
    business_id = businesses[0]['id']
    response = get_business_details(API_KEY, business_id)
    return response

# return a wordscore based on similarity of names
def get_wordscore(word_1, word_2):
    word_1 = word_1.replace('restaurant','')
    word_1 = word_1.replace('Restaurant','')
    word_2 = word_2.replace('restaurant','')
    word_2 = word_2.replace('Restaurant','')
    score = fuzz.token_sort_ratio(word_1, word_2)
    return score

# get distance between two coordinates in meters
def get_distance(coordinates_1, coordinates_2):
    distance = 0
    try: 
        distance = geopy.distance.vincenty(coordinates_1, coordinates_2).m
    except ValueError:
        return sys.maxsize
    return distance

# verify if returned restaurant is similar enough 
def is_same_restaurant(google_name, coordinates, tentative_name, tentative_coordinates):
    is_similar = False

    c1 = (coordinates['lat'], coordinates['lng'])
    c2 = (tentative_coordinates['latitude'], tentative_coordinates['longitude'])
    distance = get_distance(c1, c2)
    
    if (distance < MAXIMUM_DISTANCE) and (get_wordscore(google_name, tentative_name) >= MINIMUM_WORDSCORE): # check word similarity and distance 
        is_similar = True

    if is_similar:
        print('EQUAL', google_name, tentative_name)
    else:
        print('NOT', google_name, tentative_name)
    return is_similar

# return restaurant details in dictionary if result is found and result is valid
def create_restaurant_object(google_name, coordinates):
    response = get_yelp_restaurants(google_name, DEFAULT_CATEGORIES, coordinates, DEFAULT_RADIUS)

    is_valid = False
    tentative_name = ''
    tentative_coordinates = {}

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
        tentative_coordinates = response.get('coordinates', {'latitude': None, 'longitude':None})
    except AttributeError:
        return details 

    is_valid = is_same_restaurant(google_name, coordinates, tentative_name, tentative_coordinates) 

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

# query yelp and update entry for each existing (google) restaurant in db, 
def update_each_restaurant():

    cursor = db.restaurants.find()
    places = []
    for place in cursor:
        places.append(place)
    cursor.close()

    # temporary counter
    counter = 0

    for place in places:
        try:
            place_name = place['name']
            coordinates = place['location'] # dict with lat and lng
            place_id = place['place_id']
        except KeyError:
            print('Key Error')
        
        # temporary 
        print(counter)
        counter += 1

        details = create_restaurant_object(place_name, coordinates)
        update_db(details, place_id)

def main():
    if API_KEY is None:
        print("No API_KEY provided")
        sys.exit(0)
    update_each_restaurant()

if __name__ == '__main__':
    main()

