const statuses = ['CARD', 'LIST'];

const task = (state, action) => {
    switch (action.type) {
        case 'CHANGE_CARD_VIEW':
        //entered from info view to go to list view
            if (state.id !== action.id) {
                console.log("change card vieew not")
                return state;
            }

            let statusNum = statuses.indexOf(state.status);
            const nextStatus = 
                statusNum === 2 
                ? statuses[0] 
                : statuses[statusNum + 1];
                console.log("change card vieew")
            return {
                ...state,
                status: nextStatus,
                restaurantID: state.id 
            };
        default:
            return state;
    }
};

const restaurants = (state = [], action) => {
    switch (action.type) {
        case 'RECEIVE_POSTS':
            console.log('get post', action)
            //going back
            console.log(action.posts+"do ye have")
            return action.posts;
        case 'CHANGE_CARD_INFO':
            console.log(action.id);
            return state.filter(restaurant=>
                restaurant._id == action.id   
            );
        default:
            return state;
    }
};

export default restaurants;