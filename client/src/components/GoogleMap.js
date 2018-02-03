import React from 'react';
import { connect } from 'react-redux';
import mapStyle from "../json/mapStyle.json";
import { compose, withProps } from "recompose";
import store from '../index.js';

import {
  withScriptjs,
  withGoogleMap,
  GoogleMap,
  Marker
} from "react-google-maps";

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
  <GoogleMap defaultZoom={8} defaultCenter={{ lat: -23, lng: 150 }} 
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
                <MapMarkers/>
                {console.log(props)}
  </GoogleMap>
));

function MapMarkers(props){
  return(
      <div>
        {
          store.getState().map((restaurant) => {
            <Marker key={restaurant.id} position={{lat:-23,lng:150}} />
          })
        }
        {console.log(store.getState(),"storeed map")}
      </div>
  )
}

const mapStateToProps = (state) => {
    return { 
        markers: MapMarkers
    };
};

export default connect(mapStateToProps)(MyMapComponent);

