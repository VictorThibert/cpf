# handles information requests /restaurant queries
import flask
import geopy.distance
import logging

from bson.objectid import ObjectId
from extensions import db
from flask import Blueprint, render_template, abort, request, jsonify


restaurant = Blueprint('restaurant', __name__, url_prefix='/restaurant')

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

# get photos 
@restaurant.route('/<restaurant_id>/photo/<photo_id>')
def get_info(restaurant_id, photo_id):
    result = db.restaurants.find_one({
        'id':restaurant_id,
        'photos.filename':photo_id
    })

    photo_filepath = result[photo_id]['filepath']
    return app.send_static_file('./photos/' + photo_filepath)

# get list of n top restaurants
@restaurant.route('/get_list')
def get_list():

    # argument list
    limit = request.args.get('limit')
    coordinates = request.args.get('coordinates')
    city = request.args.get('city')
    maximum_distance = request.args.get('maximum_distance')
    minimum_score = request.args.get('minimum_score')

    # default: return 10 restaurants TODO: convert to .get('limit',10)
    if limit is None:
        limit = 10

db.restaurants.find({'rating':{'$gt':4.5}, 'yelp_review_count':{'$gt':100}},{'name':1}).limit(10)

    results = []
    for place in db.restaurants.find({}).limit(int(limit)):
        place = create_restaurant_response(place)
        results.append(place)

    return jsonify(results)

def create_restaurant_response(place):
    response = {}
    response['_id'] = str(place.get('_id'))
    response['name'] = place.get('name','')
    response['location'] = place.get('location','')
    response['formatted_phone_number'] = place.get('formatted_phone_number', '')
    response['website'] =  place.get('website', '')
    response['yelp_photos'] = place.get('yelp_photos', [])
    response['yelp_location'] = place.get('yelp_location', {})

    return response

def get_distance(coordinates_1, coordinates_2):  # coordinates of the form (a,b)
    distance = 0
    try: 
        distance = geopy.distance.vincenty(coordinates_1, coordinates_2).m
    except ValueError:
        return sys.maxsize
    return distance