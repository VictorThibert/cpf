import React from 'react';
import ReactMap from './ReactMap.js';
import { fetchRestaurants, getUserLocation } from '../actions/testActions.js';
import { connect } from 'react-redux';


class Gmap extends React.PureComponent {

    componentDidMount() {
        this.props.dispatch(getUserLocation());
    }

    componentWillMount() {
        this.props.dispatch(fetchRestaurants(this.props.fetchLimit)); // ensures that fetch is performed
    }

    render() {
        return (
            <ReactMap
                onMarkerClick={this.props.changeCard}
                restaurants={this.props.restaurants}
                center={this.props.center} 
                geolocation={this.props.coordinates}     
                defaultCenter={this.props.defaultCenter}       
            />
        )
    }
}


// this and connect ensures that this.props is set.
const mapStateToProps = (state) => { // state contains the reducer it seems
    return {
        restaurants: state.testReducer.restaurants,
        user: state.testReducer.user,
        coordinates: state.testReducer.coordinates
    }
}

export default connect(mapStateToProps)(Gmap)