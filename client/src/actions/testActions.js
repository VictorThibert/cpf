import axios from 'axios';
import metroCities from '../metroCities.json'

export const fetchRestaurants = (limit, city='montreal') => { // montreal default for now
    const url = 'https://cherrypicker.io:4000/restaurant/get_list?limit=' + limit + '&city=' + city; // TODO : clean this structure up
    console.log(url)
    return function(dispatch) {
        axios.get(url)
            .then((response) => {
                dispatch({type:'FETCH_DATA_SUCCESS', payload: response.data}) 
            })
            .catch((err) => {
                dispatch({type:'FETCH_DATA_FAILURE', payload: err})
            })
    }
}

export const getUserLocation = () => {
    return function(dispatch) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) { // gets called after location given
                const coordinates = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                
                dispatch(setUserLocation(coordinates))  ;
                dispatch(setUserCity(coordinates));
                let city = setUserCity(coordinates).payload.city;
                dispatch(fetchRestaurants(10, city));      

            }, function() {
                console.log("Error getting geolocation of user.")
            });
        } else {
            console.log("No geolocation module found.")
        }
    }
}

export const setUserLocation = (coordinates) => {
    return {
        type: "SET_USER_LOCATION",
        payload: {
            lat: coordinates.lat,
            lng: coordinates.lng
        }
    }
}

// haversine formula
const getCoordinateDistance = (coordinates1, coordinates2) => {

    const lat1 = coordinates1.lat;
    const lng1 = coordinates1.lng;
    const lat2 = coordinates2.lat;
    const lng2 = coordinates2.lng

    const p = 0.017453292519943295;    // Math.PI / 180
    const c = Math.cos;
    const a = 0.5 - c((lat2 - lat1) * p)/2 + c(lat1 * p) * c(lat2 * p) * (1 - c((lng2 - lng1) * p))/2;

    return 12742 * Math.asin(Math.sqrt(a)); // 2 * R; R = 6371 km
}

export const setUserCity = (coordinates) => {
    const maximumDistance = 35000; // meters
    let city = 'no city found';
    let currentDistance = maximumDistance;
    
    for (let index in metroCities) {
        let entry = metroCities[index]
        let entryCoordinates = {lat:entry.lat, lng: entry.lng};
        let distance = getCoordinateDistance(entryCoordinates, coordinates);
        if (distance <= maximumDistance && distance < currentDistance) { // if two cities fall within the maximum, chooses the nearest
            city = entry.city;
            currentDistance = distance
        }
    }

    return {
        type: "SET_USER_CITY",
        payload: {
            city:city
        }
    }
}

export const fetchUser = (test) => { //TODO: remove (this is only for illustrative purposes)
    return {
        type: "FETCH_USER",
        payload: {
            name:"Will"
        }
    }
}

