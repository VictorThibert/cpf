from googleplaces import GooglePlaces, types, lang
from extensions import db
import os
import uuid
import glob

API_KEY = 'AIzaSyBqBPkJ6C6GFemKwqqI8lMOuz6_Tr91bs8'

google_places = GooglePlaces(API_KEY)

def get_google_results(location='Montreal, Canada', radius=20000, limit=60):
    # You may prefer to use the text_search API, instead.
    print("get_google_results: function start")
    query_result = google_places.nearby_search(
        location=location,
        radius=radius,
        types=[types.TYPE_RESTAURANT])

    if query_result.has_attributions:
        print(query_result.html_attributions)
    num_places = 0
    while True:
        for place in query_result.places:
            num_places += 1
            if(num_places == limit): break
            place.get_details()
            yield place

        if query_result.has_next_page_token:
            query_result = google_places.nearby_search(
                pagetoken=query_result.next_page_token)
        else: break

def parse_photos(photos, limit=3):
    all_photos = []
    num = 0
    print("parsing photos")
    for photo in photos:
        num += 1
        print("parsing photo: ", photo)
        photo_obj = parse_photo(photo)
        all_photos.append(photo_obj)
        if(num == limit): break
    return all_photos
def parse_photo(photo):
    photo_inf = {}
    photo.get(maxheight=500, maxwidth=500)
    photo_inf['filename'] = photo.filename
    photo_inf['url'] = photo.url
    photo_inf['type'] = photo.mimetype
    photo_inf['id'] = save_photo(photo)
    return photo_inf

def does_name_exist(name):
    """ check if a file with that name already exists """
    return len(glob.glob('./photos/'+name+'.*')) > 0
def save_photo(photo):
    name = ""
    while True:
        name = uuid.uuid4().hex[:15]
        if(not does_name_exist(name)): break
    file_type = photo.filename.split('.')[-1]
    photo_file = open('./photos/' + name + '.'+file_type, 'wb')
    photo_file.write(photo.data)
    photo_file.close()
    return name

def add_all_data_db(get_data, limit=-1):
    data_gen = get_data(limit=limit)
    for data in data_gen:
        add_data_db(data)
def add_data_db(place):
    print("place: ", place)
    place_info = place.details
    del place_info['geometry']
    del place_info['scope']
    place_info['photos'] = parse_photos(place.photos)
    place_info['rating'] = float(place_info['rating'])
    db.restaurants.save(place_info)

def main(limit=-1):
    add_all_data_db(get_google_results, limit)

if __name__ == '__main__':
    main(limit=10)
