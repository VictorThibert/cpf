// reducers (takes actions and creates new state, which will be rerendered)

const defaultState = {
    restaurants: [],
    fetching: false,
    fetched: false,
    error: null,
    user: "joebeef"
};

const reducer = (state = defaultState, action) => {
    switch(action.type) {
        case 'FETCH_DATA': {
            console.log("FETCH_DATA action");
            return {
                ...state,
                fetching: true
            };
        }
        case 'FETCH_DATA_SUCCESS': {
            console.log("FETCH_DATA_SUCCESS action");
            return {
                ...state,
                restaurants:action.payload,
                fetching: false,
                fetched: true
            }
        }
        case 'FETCH_DATA_FAILURE': {
            console.log("FETCH_DATA_FAILURE action");
            return {
                ...state,
                error:action.payload,
                fetching: false,
            }
        }
        case 'FETCH_USER': {
            console.log("FETCH_USER action", action.payload.name)
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
