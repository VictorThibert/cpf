from flask import Blueprint, render_template, abort, request, jsonify
from bson.objectid import ObjectId
import flask
import logging
from extensions import db

restaurant = Blueprint('restaurant', __name__, url_prefix='/restaurant')
photos_path='./photos/'
logging.info("this is from the game file");

@restaurant.route('/<rest_id>/info')
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

@restaurant.route('/photos/<photo_id>')
def get_info(rest_id, photo_id):
    res = glob.glob(photos_path + photo_id+"*")
    if(len(res) == 0): return "photo id does not exist", 404
    return app.send_static_file('./photos/'+res[0])

@restaurant.route('/get_list')
def get_list():
    pass

