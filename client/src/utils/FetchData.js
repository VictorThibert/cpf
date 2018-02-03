import { changeCardInfo, removeTask, getPosts, receivePosts } from '../actions';


export const getRestaurantList = () => {
    return dispatch => {
        dispatch(getPosts)
        return fetch(`data.json`)
      .then((response) => {
        return response.json()
    })
      .then(json => dispatch(receivePosts(json)))
      .catch(error => {
        console.log("fetch error: ", error);
      })
  }
}