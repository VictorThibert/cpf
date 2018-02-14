# handles information requests /restaurant queries
import flask
import geopy.distance
import logging

from bson.objectid import ObjectId
from extensions import db
from flask import Blueprint, render_template, abort, request, jsonify


restaurant = Blueprint('restaurant', __name__, url_prefix='/restaurant')
photos_path='./photos/'
logging.info("this is from the game file");

# get restaurant information given a specific restaurant id (using MongoDB id)
@restaurant.route('/<restaurant_id>/info')
def get_restaurant_info(restaurant_id):
    _id = ObjectId(restaurant_id)
    result = db.restaurants.find_one({
        '_id': _id
    },{
        'reviews':False,
        'address_components':False
    })
    if(result == None): result = {
        '_id':"",
        "success":False
    }
    result['_id'] = str(result['_id'])
    result['success'] = True
    return jsonify(result)

@restaurant.route('/photos/<photo_id>')
def get_info(rest_id, photo_id):
    res = glob.glob(photos_path + photo_id+"*")
    if(len(res) == 0): return "photo id does not exist", 404
    return app.send_static_file('./photos/'+res[0])

# get list of n top restaurants
@restaurant.route('/get_list')
def get_list():

    result_set = []
    search_set = {}

    DEFAULT_LIMIT = 10
    DEFAULT_MAXIMUM_DISTANCE = 30000
    DEFAULT_MINIMUM_SCORE = 0

    # argument list TODO: document api
    limit = int(request.args.get('limit', DEFAULT_LIMIT))
    coordinates = request.args.get('coordinates', None) # given in the form of a string 'lat,lng' (not good to use brackets of any kind in urls)
    maximum_distance = float(request.args.get('maximum_distance', DEFAULT_MAXIMUM_DISTANCE))
    minimum_score = float(request.args.get('minimum_score', DEFAULT_MINIMUM_SCORE))

    if coordinates is not None:
        lat, lng = coordinates.split(',')
        lat, lng = [float(lat), float(lng)]
        search_set = db.restaurants.find({
            'geo_json':{'$geoWithin':{'$centerSphere':[[lng, lat], meters_to_radians(maximum_distance)]}},
            'rating':{'$gt':minimum_score}
            }).sort('rating', -1).limit(limit)
    else:
        search_set = db.restaurants.find({'rating':{'$gt':minimum_score}}).sort('rating', -1).limit(int(limit))
    
    for place in search_set:
        place = create_restaurant_response(place)
        result_set.append(place)

    return jsonify(result_set)

def create_restaurant_response(place):
    response = {}
    response['_id'] = str(place.get('_id'))
    response['name'] = place.get('name','')
    response['location'] = place.get('location','')
    response['formatted_phone_number'] = place.get('formatted_phone_number', '')
    response['website'] =  place.get('website', '')
    response['yelp_photos'] = place.get('yelp_photos', [])
    response['yelp_location'] = place.get('yelp_location', {})
    response['yelp_price'] = place.get('yelp_price', '')

    return response

def meters_to_radians(meters):
    miles = meters / 1609.34
    radians = miles / 3963.20
    return radians

