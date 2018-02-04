import React from 'react';
import { connect } from 'react-redux';
import mapStyle from "../json/mapStyle.json";
import { compose, withProps } from "recompose";
import store from '../index.js';
import {getRestaurantList} from '../utils/FetchData';
import { changeCardInfo, removeTask, getPosts, receivePosts } from '../actions';

import {
  withScriptjs,
  withGoogleMap,
  GoogleMap,
  Marker
} from "react-google-maps";

//temporary until we get users location permission
const LAT = 45.50144299999999;
const LNG = -73;

const MyMapComponent = compose(
  withProps({
    googleMapURL:
      "https://maps.googleapis.com/maps/api/js?key=AIzaSyCDQT5ml_cuuTiow547s31RHb02RKy_APs&v=3.exp&libraries=geometry,drawing,places",
    loadingElement: <div style={{ height: `100%` }} />,
    containerElement: <div style={{ height: `100vh` }} />,
    mapElement: <div style={{ height: `100%` }} />
  }),
  withScriptjs,
  withGoogleMap
)(props => (
  <GoogleMap defaultZoom={8} center={{ lat: LAT, lng: LNG}} 
             defaultOptions={{ 
                styles: mapStyle, 
                streetViewControl: false,
                scaleControl: false,
                mapTypeControl: false,
                panControl: false,
                zoomControl: false,
                rotateControl: false,
                fullscreenControl: false }} 
                style={{ position:'absolute'}}>
                  <MapMarkers restaurants={props.restaurants} />
                  {console.log(props,"googsboi")}
  </GoogleMap>
));

function MapMarkers(props){
  return(
      <div>
        {
          props.restaurants.map((restaurant) => {
            if(restaurant.location!=""){
             return (<Marker key={restaurant._id}
                      position={{ lat:restaurant.location.lat, lng:restaurant.location.lng }} 
                      onClick={()=> store.dispatch(changeCardInfo(restaurant._id))} 
                    />)
            }
          })
        }
      </div>
  )
}

const mapStateToProps = (state) => {
    return { 
      restaurants: state
    };
};

export default connect(mapStateToProps)(MyMapComponent);

