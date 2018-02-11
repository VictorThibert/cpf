# support file to update existing mongo records to include GeoJSON points

from extensions import db
from bson.objectid import ObjectId

def create_index():
	db.restaurants.create_index([('geo_json', '2dsphere')], name='geo_json_index')

def insert_geo_json():
	for restaurant in db.restaurants.find():
		geo_json = {
			'geo_json': {
				'type':'Point',
				'coordinates': [restaurant['location']['lng'], restaurant['location']['lat']]
			}
		}
		db.restaurants.update_one({'_id':ObjectId(restaurant['_id'])}, {'$set':geo_json}, upsert=False)

def main():
	insert_geo_json()
	create_index()

if __name__ == '__main__':
	main()