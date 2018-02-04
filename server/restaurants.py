# handles information requests /restaurant queries

from flask import Blueprint, render_template, abort, request, jsonify
from bson.objectid import ObjectId
import flask
import logging
from extensions import db

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
