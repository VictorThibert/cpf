from flask import Blueprint, render_template, abort, request, jsonify
import flask
import logging

restaurant = Blueprint('restaurant', __name__, url_prefix='/restaurant')

logging.info("this is from the game file");

@restaurant.route('/<id>/info')
def getGameInformation(id):
    pass

@restaurant.route('/get_list')
def getGameInformation():
    pass

