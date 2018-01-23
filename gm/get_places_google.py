# get all restaurants using Google API and recursive grid to subdivide

import time
import math
from googleplaces import GooglePlaces, types, lang
import geopy
import geopy.distance
from geopy.distance import VincentyDistance

API_KEY = 'AIzaSyCDQT5ml_cuuTiow547s31RHb02RKy_APs'

google_places = GooglePlaces(API_KEY)

all_restaurants = []


# initial parameters (for Montreal)
TL = (45.7, -74)
BR = (45.4, -73.4)

# TODO: issue with converting grid to lat/lng due to curvature of earth
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
    c1 = (TL[0] - (TL[0]-BR[0])/4  ,   TL[1] + (BR[1]-TL[1])/4)
    c2 = (TL[0] - (TL[0]-BR[0])/4  ,   TL[1] + 3*(BR[1]-TL[1])/4)
    c3 = (TL[0] - 3*(TL[0]-BR[0])/4  ,   TL[1] + (BR[1]-TL[1])/4)
    c4 = (TL[0] - 3*(TL[0]-BR[0])/4  ,   TL[1] + 3*(BR[1]-TL[1])/4)
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







# must be able to convert from latitude and longtitude into meters

def main():
    traverse_quadrant(TL, BR, all_restaurants)

def get_places_at_location(location, radius):

    print("location: ", location)

    current_count = 0
    found_restaurants = []

    # TODO: find a more elegant structure instead of this ugly mess

    query_result = google_places.nearby_search(
        radius = radius,
        location = location,
        keyword = '',    
        types = [types.TYPE_RESTAURANT]
    )

    for place in query_result.places:
        current_count += 1
        found_restaurants.append(place.name)
        print(current_count, place.name)

    # Are there any additional pages of results?
    # time.sleep is required in order to avoid invalid request errorss
    time.sleep(2)
    if query_result.has_next_page_token:
        qn2 = google_places.nearby_search(pagetoken=query_result.next_page_token)
        # 20-40
        for place in qn2.places:
            current_count += 1
            found_restaurants.append(place.name)
            print(current_count, place.name)

        # Are there any additional pages of results?
        time.sleep(2)
        if qn2.has_next_page_token:
            qn3 = google_places.nearby_search(pagetoken=qn2.next_page_token)
            # 40-60
            for place in qn3.places:
                current_count += 1
                found_restaurants.append(place.name)
                print(current_count, place.name)

    return found_restaurants

def convert_coordinates_to_string(coordinate):
    return ','.join([str(coordinate['lat']),str(coordinate['lng'])])

def find_radius(square_length):
    return 0.5 * math.sqrt(2*(square_length)**2)


if __name__ == '__main__':
    main()