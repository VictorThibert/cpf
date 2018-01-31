# get all restaurants using Google API and recursive grid to subdivide

# basic imports
import time
import math
import os

# from googleplaces import GooglePlaces, lang, types
from custom_wrapper import GooglePlaces, lang
import geopy
import geopy.distance
from geopy.distance import VincentyDistance

# database related imports
# from extensions import db
import uuid

# get API key from environment. TODO: use env file instead
API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
google_places = GooglePlaces(API_KEY)

all_restaurants = []

# initial parameters (for Montreal)
TL = (45.55, -73.7)
BR = (45.4, -73.5)
sleep_time = 0 # 0 if using .get_details, 2 if not

# TODO: issue with converting grid to lat/lng due to curvature of earth
# TODO: standardize coordinate represenation (dictionry, vs (x,y) pair, etc.)
# verify that current approximation works on city scales

def traverse_quadrant(TL, BR, all_restaurants):

    # coordinate measurements
    latitude_midpoint = (TL[0] + BR[1])/2
    longitude_midpoint = (TL[0] + BR[1])/2

    # four points on quadrant (in lat/lng)
    TL = (TL[0], TL[1])
    TR = (TL[0], BR[1])
    BR = (BR[0], BR[1])
    BL = (BR[0], BR[1])

    # side lengths in meters
    horizontal = geopy.distance.vincenty(TL, TR).km * 1000
    vertical = geopy.distance.vincenty(TL, BL).km * 1000

    # determine the centers for the 4 circles in terms of lat/lng
    c1 = (TL[0] - (TL[0]-BR[0])/4, TL[1] + (BR[1]-TL[1])/4)
    c2 = (TL[0] - (TL[0]-BR[0])/4, TL[1] + 3 * (BR[1]-TL[1])/4)
    c3 = (TL[0] - 3 * (TL[0]-BR[0])/4, TL[1] + (BR[1]-TL[1])/4)
    c4 = (TL[0] - 3 * (TL[0]-BR[0])/4, TL[1] + 3 * (BR[1]-TL[1])/4)
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
        print("Center", center, "Radius", radius)
        found_restaurants = get_places_at_location(center, radius)

        # subdivide if too many points in quadrant
        if len(found_restaurants) >= 60:
            traverse_quadrant(TL_2[x], BR_2[x], all_restaurants)

        else:
            all_restaurants.extend(found_restaurants)
            add_to_db(found_restaurants)



def get_places_at_location(location, radius):

    print("location: ", location)
    current_count = 0
    found_restaurants = []
   
    query_result = google_places.nearby_search(
        radius = radius,
        location = location,
        keyword = '',    
        types = ['restaurant']
    )

    while True:
        for place in query_result.places:
            current_count += 1
            place.get_details()
            found_restaurants.append(place)
            print(current_count, place)

        if query_result.has_next_page_token:
            time.sleep(sleep_time)
            query_result = google_places.nearby_search(pagetoken=query_result.next_page_token)
        else: 
            break

    return found_restaurants

def convert_coordinates_to_string(coordinate):
    return ','.join([str(coordinate['lat']), str(coordinate['lng'])])

def find_radius(square_length):
    return 0.5 * math.sqrt(2 * square_length ** 2)

def main():
    traverse_quadrant(TL, BR, all_restaurants)


if __name__ == '__main__':
    main()