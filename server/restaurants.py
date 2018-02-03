# handles information requests /restaurant queries

from flask import Blueprint, render_template, abort, request, jsonify
from bson.objectid import ObjectId
import flask
import logging
from extensions import db

restaurant = Blueprint('restaurant', __name__, url_prefix='/restaurant')

logging.info("this is from the game file");

@restaurant.route('/<restaurant_id>/info')
def get_rest_info(rest_id):
    """ gets info for a given restaurant """
    _id = ObjectId(rest_id)
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

@restaurant.route('/<restaurant_id>/photo/<photo_id>')
def get_info(rest_id, photo_id):
    result = db.restaurant.find_one({
        'id':rest_id,
        'photos.filename':photo_id
    })

    photo_filepath = result[photo_id]['filepath']
    return app.send_static_file('./photos/'+photo_filepath)

@restaurant.route('/get_list')
def get_list():
    pass

