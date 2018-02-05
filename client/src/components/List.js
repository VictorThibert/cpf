import React from 'react';
import { connect } from 'react-redux';
import RestaurantList from './RestaurantList';
import InfoCard from './InfoCard';
import store from '../index';
import {getRestaurantList} from '../utils/FetchData';
import { changeCardInfo, removeTask, getPosts, receivePosts } from '../actions';


// infoCard getRestaurantList is passed for the back button to refetch posts
function List (props) {
    return (
        <div className={`restaurantList header`}>
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

