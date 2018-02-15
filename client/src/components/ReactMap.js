/* eslint-disable no-undef */
// this above line is critical, do not remove 

import React from 'react';
import { compose, withProps } from 'recompose';
import { withScriptjs, withGoogleMap, GoogleMap, Marker, Size } from 'react-google-maps';
import mapStyle from '../mapStyle.json';



const ReactMap = compose(
  withProps({
    googleMapURL: 'https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places',
    loadingElement: <div style={{ height: '100%' }} />,
    containerElement: <div style={{ height: '100vh' }} />,
    mapElement: <div style={{ height: '100%' }} />,
  }),
  withScriptjs,
  withGoogleMap
)((props) =>
    <GoogleMap
        defaultZoom={13}
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

const radishUrl = (i, number_of_restaurants) => {
    const prefix = 'https://i.cubeupload.com/'
    const urls = ['ThtjvX.png', 'AgvJ9m.png', '8KjxI6.png', 'A1SNk0.png', 'G9jJuq.png', 'UvY6j5.png', '2i3cWq.png', 'Z2fQ7e.png', 'fwblGv.png', 'Lfuk8Z.png'];
    const bins = Math.floor(number_of_restaurants/urls.length);
    
    return prefix + urls[Math.floor(i/(bins))]
}


const generateMarkers = (props) => {
    const restaurants = props.restaurants;


    // temporary sort for marker testing
    restaurants.sort((a,b) => {
        return a.location.lng - b.location.lng
    })
    let i = 0

    const n = 6; // temporary divisor for icon size
    const image = {
        url: radishUrl(),
        scaledSize: new google.maps.Size(198/n, 281/n)
    };

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
            icon = {{
                url: radishUrl(i++, restaurants.length),
                scaledSize: new google.maps.Size(198/n, 281/n)
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

