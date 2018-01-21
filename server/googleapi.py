from googleplaces import GooglePlaces, types, lang
from extensions import db

YOUR_API_KEY = 'AIzaSyBqBPkJ6C6GFemKwqqI8lMOuz6_Tr91bs8'
google_places = GooglePlaces(YOUR_API_KEY)

def get_google_results(location='Montreal, Canada', radius=20000):
    # You may prefer to use the text_search API, instead.
    print("get_google_results: function start")
    query_result = google_places.nearby_search(
	location=location,
	radius=radius,
	types=[types.TYPE_RESTAURANT])

    if query_result.has_attributions:
        print(query_result.html_attributions)

    while True:
        print("get_google_results: loop")
        for place in query_result.places:
            place.get_details()
            yield place

        if query_result.has_next_page_token:
            query_result = google_places.nearby_search(
        	    pagetoken=query_result.next_page_token)
        else: break
    # Are there any additional pages of results?
    if query_result.has_next_page_token:
        query_result_next_page = google_places.nearby_search(
                pagetoken=query_result.next_page_token)

def add_all_data_db(get_data):
    data_gen = get_data()
    print("data_gen: ", data_gen)
    for data in data_gen:
        add_data_db(data)
def add_data_db(place):
    print("place: ", place)
    place_info = place.details
    del place_info['geometry']
    del place_info['scope']


def main():
    add_data_db(get_google_results)

if __name__ == '__main__':
    main()
