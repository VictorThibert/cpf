import axios from 'axios';

export function fetchRestaurants(limit) {
	const url = 'http://cherrypicker.io:4000/restaurant/get_list?limit=' + '100';

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

export function fetchUser() {
	return {
		type: "FETCH_USER",
		payload: {
			name:"Will"
		}
	}
}