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

# move to env file
API_KEY = os.environ.get('YELP_API_KEY')

# API constants
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/' 


# Defaults for our simple example.
DEFAULT_TERM = 'Saint Bock'
DEFAULT_LOCATION = 'Montreal, Canada'
DEFAULT_COORDINATES = {'lat':45.515429687499996,'lng':-73.56484375}
SEARCH_LIMIT = 3
DEFAULT_RADIUS = 100 # in meters



def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, categories, coordinates, radius):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        # 'location': location.replace(' ', '+'),
        'latitude': coordinates['lat'],
        'longitude': coordinates['lng'],
        'radius': radius,
        'limit': SEARCH_LIMIT,
        'categories': categories,
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, location, categories, coordinates, radius):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, term=term, categories=categories, coordinates=coordinates, radius=radius)

    businesses = response.get('businesses')

    if not businesses:
        print('No businesses for {0} in {1}, {2} found.'.format(term, coordinates['lat'], coordinates['lng']))
        return

    # recover first business
    business_id = businesses[0]['id']

    print('{0} businesses found, querying business info for the top result "{1}" ...'.format(len(businesses), business_id))

    # get more information about specific business
    response = get_business(API_KEY, business_id)

    print('Result for business "{0}" found:'.format(business_id))
    pprint.pprint(response, indent=2)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM, type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location, "restaurants", DEFAULT_COORDINATES, DEFAULT_RADIUS)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()