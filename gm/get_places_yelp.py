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

API_KEY = os.environ.get('YELP_API_KEY')


# api constants
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/' 

SEARCH_LIMIT = 5
DEFAULT_RADIUS = 50 # in meters
DEFAULT_CATEGORIES = "restaurants"

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

def query_api(term, categories, coordinates, radius):
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

def search_yelp(place_name, location):
    response = query_api(place_name, DEFAULT_CATEGORIES, location, DEFAULT_RADIUS)

    # only keep relevant details
    details = {}
    try:
        details['yelp_review_count'] = response['review_count']
        details['yelp_categories'] = response['categories']
        details['yelp_id'] = response['id']
        details['yelp_photos'] = response['photos']
        details['yelp_rating'] = response['rating']
        details['yelp_url'] = response['url']
        details['yelp_location'] = response['location']
        details['yelp_name'] = response['name']
    except (TypeError, KeyError) :
        details['yelp_review_count'] = None
        details['yelp_categories'] = []
        details['yelp_id'] = None
        details['yelp_photos'] = []
        details['yelp_rating'] = None
        details['yelp_url'] = None
        details['yelp_location'] = None
        details['yelp_name'] = None
    return details

# for each restaurant in db, query yelp and update with additional information
def query_db():
    for place in db.restaurants.find():
        try:
            place_name = place['name']
            location = place['location']
            place_id = place['place_id']
        except KeyError:
            print('Key Error')

        print(place_name, location)

        details = search_yelp(place_name, location)

        update_db(details, place_id)

def main():
    if API_KEY is None:
        print("No API_KEY provided")
        sys.exit(0)
    query_db()

if __name__ == '__main__':
    main()

