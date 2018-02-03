let nextTaskId = 0;

export const addRestaurant = ({ text, executor, cost, image, lat,lng }) => {
    return {
        type: 'ADD_RESTAURANT',
        id: (nextTaskId++).toString(),
        text,
        executor,
        cost,
        lat,
        lng
    };
};

export const removeRestaurant = (id) => {
    return {
        type: 'REMOVE_RESTAURANT',
        id
    };
};

export const changeCardInfo = (id, cost, image, text,lat,lng) => {
    return {
        type: 'CHANGE_CARD_INFO',
        id,
        cost,
        image,
        text,
        lat,
        lng
    };
};

export const getPosts = (subreddit,json) => {
    console.log("getposteed")
    return {
        type: 'GET_POSTS', 
        posts: json
    }
}

export const receivePosts = (json) => {
    console.log("receivedAt",json)
    return {
        type: "RECEIVE_POSTS",
        posts: json,
        receivedAt: Date.now()
    }
}