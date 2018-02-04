# ranking algorithm

from extensions import db

def average_city_rating(city):
	average_rating = 0
	response = db.restaurants.aggregate([{'$group':{'_id':'$city','average_rating':{'$avg':'$rating'}}}])

	# traverse through cursor to find particular city id
	for cities in response:
		if str(cities.get('_id')) == str(city):
			try:
				average_rating = cities['average_rating']
			except KeyError:
				print('No average rating found for city: ', city)
			return average_rating

	print("City not found in response", average_rating)
	return average_rating

def get_weighted_rating(rating, review_count, city, city_rating=None):
	m = 20 # minimum number of ratings required

	if city_rating == None:
		city_rating = average_city_rating(city) # mean vote across city

	weighted_rating =  (review_count / (review_count + m)) * rating + (m / (review_count + m)) * city_rating
	
	return weighted_rating

def get_google_rating(place):
	return place.get('rating', 0.0)

def get_yelp_rating(place):
	return place.get('yelp_rating', 0.0)

def get_combined_rating(ratings):
	# remove 0.0 ratings
	ratings = list(filter(lambda x: x > 0.0, ratings))
	if len(ratings) == 0:
		return 0
	# ratings as an array 
	return round(sum(ratings)/len(ratings),2)

def main():
	city = 'montreal'

if __name__ == '__main__':
	main()