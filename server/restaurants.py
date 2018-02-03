# handles information requests /restaurant queries

from flask import Blueprint, render_template, abort, request, jsonify
from bson.objectid import ObjectId
import flask
import logging
from extensions import db

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
    limit = request.args.get('limit')

    # default: return 10 restaurants
    if limit is None:
        limit = 10

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