import React from 'react';
import ReactMap from './ReactMap.js';
import { fetchRestaurants, getUserLocation } from '../actions/testActions.js';
import { connect } from 'react-redux';


class Gmap extends React.PureComponent {

    constructor() {
        super();
        this.state = {
            'city':'montreal'
        }
    }

    componentDidMount() {
    }

    componentWillMount() {
        this.props.dispatch(getUserLocation());
        this.props.dispatch(fetchRestaurants(this.props.fetchLimit, this.props.city)); // ensures that fetch is performed
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
        coordinates: state.testReducer.coordinates,
        city: state.testReducer.city
    }
}

export default connect(mapStateToProps)(Gmap)