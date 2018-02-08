import React from 'react';
import { compose, withProps } from 'recompose';
import { withScriptjs, withGoogleMap, GoogleMap, Marker } from 'react-google-maps';
import mapStyle from '../mapStyle.json';

const ReactMap = compose(
  withProps({
    googleMapURL: 'https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places',
    loadingElement: <div style={{ height: '100%' }} />,
    containerElement: <div style={{ height: '800px' }} />,
    mapElement: <div style={{ height: '100%' }} />,
  }),
  withScriptjs,
  withGoogleMap
)((props) =>
    <GoogleMap
        defaultZoom={12}
        defaultCenter={{ lat: 45.5, lng: -73.59 }}
        defaultOptions={{ 
        styles: mapStyle, 
        streetViewControl: false,
        scaleControl: false,
        mapTypeControl: false,
        panControl: false,
        zoomControl: false,
        rotateControl: false,
        fullscreenControl: false }} 
        style={{ position:'absolute'}}
        ref={(map) => map && map.panTo({lat: props.lat,lng: props.lng})}
    >

    {generateMarkers(props)}
    </GoogleMap>
)


const generateMarkers = (props) => {
    const restaurants = props.restaurants;

    const restaurantMarkers = restaurants.map(restaurant => 
        <Marker 
            position = {{ 
                lat: restaurant.location.lat, 
                lng: restaurant.location.lng
            }} 
            key = {restaurant._id}
            onClick = {() => {
                props.panTo(restaurant.location.lat, restaurant.location.lng)
                props.onMarkerClick(restaurant)
            }}
        />
    )
    
    return (
        <div>
            {restaurantMarkers}
        </div>
    )
    
    
}

export default ReactMap;

