from googleplaces import GooglePlaces, types, lang
from extensions import db

YOUR_API_KEY = 'AIzaSyBqBPkJ6C6GFemKwqqI8lMOuz6_Tr91bs8'
google_places = GooglePlaces(YOUR_API_KEY)

def get_google_results(location='Montreal, Canada', radius=20000):
    # You may prefer to use the text_search API, instead.
    query_result = google_places.nearby_search(
        location=location,
        radius=radius,
        types=[types.TYPE_RESTAURANT])

    if query_result.has_attributions:
        print(query_result.html_attributions)

    while True:
        for place in query_result.places:
            place.get_details()
            yield place

        if query_result.has_next_page_token:
            query_result = google_places.nearby_search(
                    pagetoken=query_result.next_page_token)
        else: break
        """
        # Returned places from a query are place summaries.
        print place.name
        print place.geo_location
        print place.place_id

        # The following method has to make a further API call.
        place.get_details()
        # Referencing any of the attributes below, prior to making a call to
        # get_details() will raise a googleplaces.GooglePlacesAttributeError.
        print place.details # A dict matching the JSON response from Google.
        print place.local_phone_number
        print place.international_phone_number
        print place.website
        print place.url

        # Getting place photos

        for photo in place.photos:
            # 'maxheight' or 'maxwidth' is required
            photo.get(maxheight=500, maxwidth=500)
            # MIME-type, e.g. 'image/jpeg'
            photo.mimetype
            # Image URL
            photo.url
            # Original filename (optional)
            photo.filename
            # Raw image data
            photo.data
        """


    # Are there any additional pages of results?
    if query_result.has_next_page_token:
        query_result_next_page = google_places.nearby_search(
                pagetoken=query_result.next_page_token)

def add_all_data_db(get_data):
    data_gen = get_data()
    for data in data_gen:
        add_data_db(data)
def add_data_db(place):
    place_info = place.details
    del place_info['geometry']
    del place_info['scope']

    pass

def main():
    add_data_db(get_google_results)
    pass

if __name__ == '__main__':
    main()
