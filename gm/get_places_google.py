# get all restaurants using Google API and recursive grid to subdivide

# basic imports
import geopy
import geopy.distance
import glob
import json
import math
import os
import sys
import time
import uuid
from custom_wrapper import GooglePlaces, lang # needed to avoid certiain bugs
from extensions import db
from geopy.distance import vincenty, Point

# get API key from environment. TODO: use env file instead
API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')
GOOGLE_PLACES = GooglePlaces(API_KEY)
DEFAULT_INSCRIPTION_RADIUS = 15000
SLEEP_TIME = 2 # 0 if using .get_details, 2 if not
CITY = sys.argv[1]

# TODO: convert coordinates from tuple (lat,lng) to proper {lat:lat, lng:lng}
# TODO: issue with converting grid to lat/lng due to curvature of earth
# TODO: standardize coordinate represenation (dictionry, vs (x,y) pair, etc.)
# TODO: optimize using last size bumping (see algorithm specifications)

# segments quadrant into subsections to recursively look for restaurants
def traverse_quadrant(TL, BR):
    # four points on quadrant (in lat/lng)
    TL = (TL[0], TL[1])
    TR = (TL[0], BR[1])
    BR = (BR[0], BR[1])
    BL = (BR[0], BR[1])

    # side lengths in meters
    horizontal = geopy.distance.vincenty(TL, TR).km * 1000
    vertical = geopy.distance.vincenty(TL, BL).km * 1000

    # determine the centers for the 4 circles in terms of lat/lng
    c1 = (TL[0] - (TL[0] - BR[0]) / 4, TL[1] + (BR[1] - TL[1]) / 4)
    c2 = (TL[0] - (TL[0] - BR[0]) / 4, TL[1] + 3 * (BR[1] - TL[1]) / 4)
    c3 = (TL[0] - 3 * (TL[0] - BR[0]) / 4, TL[1] + (BR[1] - TL[1]) / 4)
    c4 = (TL[0] - 3 * (TL[0] - BR[0]) / 4, TL[1] + 3 * (BR[1] - TL[1]) / 4)
    centers = [c1,c2,c3,c4]

    # store arrays for the TLs and BRs for the next four sub-quadrants
    TL_2 = [
        (TL[0], TL[1]),
        (TL[0], TL[1] + (BR[1]-TL[1])/2),
        (TL[0] - (TL[0]-BR[0])/2, TL[1]),
        (TL[0] - (TL[0]-BR[0])/2, TL[1] + (BR[1]-TL[1])/2)
    ]
    BR_2 = [
        (TL[0] - (TL[0]-BR[0])/2, TL[1] + (BR[1]-TL[1])/2),
        (TL[0] - (TL[0]-BR[0])/2, BR[1]),
        (BR[0], TL[1] + (BR[1]-TL[1])/2),
        (BR[0], BR[1])
    ]

    # calculate associated radius for each sub-quadrant
    radius = find_radius(max(vertical, horizontal)/2)

    # attempt four quadrants TL TR BL BR
    for x in range(0,4):
        center = ','.join([str(centers[x][0]), str(centers[x][1])])
        print('Center', center, 'Radius', radius)
        found_restaurants = get_places_at_location(center, radius)

        # subdivide if too many points in quadrant
        if len(found_restaurants) >= 60:
            traverse_quadrant(TL_2[x], BR_2[x])
        else:
            add_to_db(found_restaurants)

# calls google places api with coordinates and radius 
def get_places_at_location(location, radius):
    print('location: ', location)
    current_count = 0
    found_restaurants = []
    query_result = GOOGLE_PLACES.nearby_search(
        radius = radius,
        location = location,
        keyword = '',
        types = ['restaurant']
    )

    while True:
        for place in query_result.places:
            current_count += 1
            found_restaurants.append(place)
            print(current_count, place.name)

        if query_result.has_next_page_token:
            time.sleep(2)
            query_result = GOOGLE_PLACES.nearby_search(pagetoken=query_result.next_page_token)
        else:
            break

    return found_restaurants

# verifies if entry already exists in db
def exists_in_db(place):
    return db.montreal.find({'place_id':place['place_id']}).count() > 0

# TODO : fix photos collection
# rewrites place object to match cpf needs
def parse_place(place):
    # set place to its details
    place = place.details

    # reduce number of photos and parse
    # photos = parse_photos(place.get('photos',{}))

    # converting geometry into location
    place['location'] = place['geometry']['location']
    place['location']['lat'] = float(place['location']['lat'])
    place['location']['lng'] = float(place['location']['lng'])

    #place['photos'] = photos

    # convert rating to a float
    if 'rating' in place:
        place['rating'] = float(place['rating'])
    else:
        place['rating'] = float(0)

    # remove unnecessary entries
    del place['scope']
    del place['adr_address']
    del place['icon']
    del place['geometry']

    # add city name
    place['city'] = CITY

    place['geo_json'] = {
        'type':'Point',
        'coordinates': [float(place['location']['lng']), float(place['location']['lat'])]
    }

    return place

def parse_photos(photos, limit=3):
    all_photos = []
    count = 0
    for photo in photos:
        count += 1
        photo_obj = format_photo(photo)
        all_photos.append(photo_obj)
        if(count >= limit): break
    return all_photos

def format_photo(photo):
    photo_inf = {}
    photo.get(maxheight=500, maxwidth=500)
    photo_inf['filename'] = photo.filename
    photo_inf['url'] = photo.url
    photo_inf['type'] = photo.mimetype
    photo_inf['id'] = save_photo(photo)
    return photo_inf

def does_name_exist(name):
    return len(glob.glob('./photos/'+name+'.*')) > 0

def save_photo(photo):
    name = ''
    while True:
        name = uuid.uuid4().hex[:15]
        if(not does_name_exist(name)): break
    file_type = photo.filename.split('.')[-1]
    photo_file = open('./photos/' + name + '.'+file_type, 'wb')
    photo_file.write(photo.data)
    photo_file.close()
    return name

def add_to_db(found_restaurants):
    for place in found_restaurants:
        place.get_details()

        if(exists_in_db(place.details)): continue
        place = parse_place(place)

        db.restaurants.update_one(
            {'place_id':place['place_id']},
            {'$set':
                place
            },
                upsert=True
            )

def convert_coordinates_to_string(coordinate):
    return ','.join([str(coordinate['lat']), str(coordinate['lng'])])

def find_radius(square_length):
    return 0.5 * math.sqrt(2 * square_length ** 2)

def get_corners(coordinates, radius=DEFAULT_INSCRIPTION_RADIUS): #inscribed square in circle
    km = radius/1000
    TL_point = vincenty(kilometers=km).destination(Point(coordinates[0], coordinates[1]), 315) # northwest
    BR_point = vincenty(kilometers=km).destination(Point(coordinates[0], coordinates[1]), 135) # southeast

    TL = (TL_point[0], TL_point[1])
    BR = (BR_point[0], BR_point[1])

    return (TL, BR)

def get_city_coordinates(city):
    cities = []
    with open('metro_cities.json') as json_data:
        cities = json.load(json_data)
    
    for entry in cities:
        if entry['city'] == city:
            return (entry['lat'], entry['lng'])

    print('City ', city, ' not found')
    sys.exit(0)

def main():
    city = sys.argv[1]
    print('Getting city: ', city)

    city_coordinates = get_city_coordinates(city)
    (TL, BR) = get_corners(city_coordinates, DEFAULT_INSCRIPTION_RADIUS)

    print(TL, BR, city_coordinates)
    traverse_quadrant(TL, BR)

if __name__ == '__main__':
    main()
