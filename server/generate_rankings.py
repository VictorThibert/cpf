# generates ranking list for restaurants
# currently Bayesian weighted score

from algorithm import get_weighted_rating, get_google_rating, get_yelp_rating, get_combined_rating
from extensions import db

def query_db(city):
    response = db.restaurants.find({'city':{'$eq':city}})
    return response

def insert_weighted_ratings(reference, name, rating):
    db.rankings.update_one(
        {'reference':reference},
        {'$set':{
                'name': name,
                'rating':rating
            }
            
        },
            upsert=True
    )


def main():
    city = 'montreal'
    response = query_db(city)

    # temporary offset TODO: fix
    # offset if yelp_review_count exists
    offset = 0.7

    for place in response:
        yelp_rating = get_yelp_rating(place)
        yelp_review_count = place.get('yelp_review_count', 0.0)
        google_rating = get_google_rating(place)

        weighted_yelp_rating = 0.0
        weighted_google_rating = 0.0

        # scale the yelp rating
        if yelp_rating is not None and yelp_review_count is not None:
            weighted_yelp_rating = get_weighted_rating(yelp_rating, yelp_review_count, city)
        
        # scale the google rating
        if google_rating is not None:
            if yelp_review_count is not None:
                weighted_google_rating = get_weighted_rating(google_rating, yelp_review_count, city)
            else:
                weighted_google_rating = google_rating - offset

        combined_rating = get_combined_rating([weighted_yelp_rating, weighted_google_rating])

        reference = place.get('_id')
        name = place.get('name')
        insert_weighted_ratings(reference, name, combined_rating)




if __name__ == '__main__':
    main()