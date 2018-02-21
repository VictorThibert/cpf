import axios from 'axios';

export const fetchRestaurants = (limit) => {
    const url = 'http://cherrypicker.io:4000/restaurant/get_list?limit=' + limit;

    return function(dispatch) {
        axios.get(url)
            .then((response) => {
                dispatch({type:'FETCH_DATA_SUCCESS', payload: response.data}) //dispatches an action???
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
                
                dispatch(setUserLocation(coordinates))           
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

export const fetchUser = (test) => { //TODO: remove (this is only for illustrative purposes)
    return {
        type: "FETCH_USER",
        payload: {
            name:"Will"
        }
    }
}

