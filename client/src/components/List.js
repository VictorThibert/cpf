import React from 'react';
import { connect } from 'react-redux';
import { changeCardInfo, removeTask, getPosts, receivePosts } from '../actions';
import RestaurantList from './RestaurantList';
import InfoCard from './InfoCard';
import store from '../index.js';


function getRestaurantList(){
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

// infoCard getRestaurantList is passed for the back button to refetch posts
function List (props) {
    return (
        <div className={`list ${status.toLowerCase()}-list`}>
            <h5>{props.children} <span>{props.restaurants.length}</span></h5>
            <h1>{props.restaurantID} dog </h1>
            {
            (props.restaurants.length>1)?
            props.restaurants.map((restaurant) => 
                <RestaurantList 
                    key={restaurant.id}
                    {...restaurant}
                    onChangeClick={props.showRestaurantInfo}/>
            ):  
                <InfoCard 
                    restaurantInfo={store.getState()} 
                    onChangeClick={ ()=> store.dispatch(getRestaurantList())} /> 
            }
        </div>
    )
}

const mapStateToProps = (state, ownProps) => {
    //filter by location for restaurants to be stored
    return { 
        restaurants: state
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        showRestaurantInfo: (id) => {
            dispatch(changeCardInfo(id));
        }
    };
};

export default connect(
    mapStateToProps, 
    mapDispatchToProps
)(List);

