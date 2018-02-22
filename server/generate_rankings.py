# generates ranking list for restaurants
# currently Bayesian weighted score

import sys

from algorithm import get_weighted_rating, get_google_rating, get_yelp_rating, get_combined_rating
from extensions import db
from bson.objectid import ObjectId

# get all restaurants for a given city
def get_all_restaurants_cursor(city):
    response = db.restaurants.find({'city':{'$eq':city}})
    return response

# update the db with the weighted ratings
def insert_weighted_ratings(object_id, rating):
    db.restaurants.update_one(
        {'_id':ObjectId(object_id)},
        {'$set':{
                'rating_v1':rating
            }
            
        }
    )

def main():
    city = sys.argv[1]
    response = get_all_restaurants_cursor(city)

    # temporary offset TODO: fix
    # offset if yelp_review_count exists
    offset = 2.0

    for place in response:
        yelp_rating = get_yelp_rating(place) # raw yelp rating
        yelp_review_count = place.get('yelp_review_count', 0.0) 

        google_rating = get_google_rating(place)

        weighted_yelp_rating = 0.0
        weighted_google_rating = 0.0

        # scale the yelp rating
        if yelp_rating is not None and yelp_review_count is not None:
            weighted_yelp_rating = get_weighted_rating(yelp_rating, yelp_review_count, city)
        
        # scale the google rating
        if google_rating is not None and yelp_review_count is not None:
            if yelp_review_count is not None:
                weighted_google_rating = get_weighted_rating(google_rating, yelp_review_count, city)
            else: # no yelp review count
                weighted_google_rating = google_rating - offset

        combined_rating = get_combined_rating([weighted_yelp_rating, weighted_google_rating])

        object_id = place.get('_id')
        
        print(place.get('name',''), combined_rating)
        insert_weighted_ratings(object_id, combined_rating)

if __name__ == '__main__':
    main()