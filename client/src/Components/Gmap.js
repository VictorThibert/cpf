import React from 'react';
import ReactMap from './ReactMap.js';
import { fetchUser, fetchRestaurants } from '../actions/testActions.js';
import { connect } from 'react-redux';


class Gmap extends React.PureComponent {
    state = {
        isMarkerShown: true,
        lat: 45.5,
        lng: -73.59
    }

    componentDidMount() {
    }

    componentWillMount() {
        this.props.dispatch(fetchRestaurants(10)); // ensures that fetch is performed
    }

    delayedShowMarker = (time) => {
        setTimeout(() => {
            this.setState({ isMarkerShown: true })
        }, time)
    }

    handleMarkerClick = (restaurant) => {
        this.props.changeCard(restaurant);
    }

    panTo = (lat, lng) => {
        this.setState({lat:lat, lng:lng});
    }


    render() {
        return (
            <ReactMap
                isMarkerShown={this.state.isMarkerShown}
                onMarkerClick={this.handleMarkerClick}
                restaurants={this.props.restaurants}
                panTo={this.panTo.bind(this)}
                lat={this.state.lat}
                lng={this.state.lng}
            />
        )
    }
}


// this and connect ensures that this.props is set.
const mapStateToProps = (state) => { // state contains the reducer it seems
    return {
        restaurants: state.testReducer.restaurants,
        user: state.testReducer.user
    }
}

export default connect(mapStateToProps)(Gmap)