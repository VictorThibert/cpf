// reducers (takes actions and creates new state, which will be rerendered)

const defaultState = {
    restaurants: [],
    error: null,
    user: "joebeef",
    coordinates: {
        lat: 40, 
        lng:-73.59
    }
};

const reducer = (state = defaultState, action) => {
    switch(action.type) {
        case "FETCH_DATA_SUCCESS": {
            return {
                ...state,
                restaurants:action.payload,
            }
        }
        case "FETCH_DATA_FAILURE": {
            return {
                ...state,
                error:action.payload,
            }
        }
        case "SET_USER_LOCATION": {
            return {
                ...state,
                coordinates:action.payload
            }
        }
        case "SET_USER_CITY": {
            return {
                ...state,
                city:action.payload.city
            }
        }
        case "FETCH_USER": {
            return {
                ...state,
                user:action.payload.name
            }
        }
        default: {
            break;
        }
    }
    return state
}

export default reducer
