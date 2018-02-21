import React, { Component } from 'react';

import Gmap from './components/Gmap';
import CardCustom from './components/CardCustom.js';
import 'semantic-ui-css/semantic.min.css';

class App extends Component {

  constructor() {
    super();
    
    // default starting card values
    this.state = {
      restaurantName: '',
      image1: '',
      price:'',
      description:'',
      website:'',
      lat:45.5017, // default to montreal for now
      lng:-73.5673
    }
  }


  locateUser() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) { // gets called after location given
        const pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };

        this.setState({
          lat:pos.lat,
          lng:pos.lng
        })

        // find out city
        // geocodeLatLng(geocoder, pos);
      }, function() {
        // handleLocationError(true, map.getCenter());
      });
    } else {
      // pass 
    }
  }

  changeCard(restaurant) {
    this.locateUser();
    this.setState({
      restaurantName:restaurant.name,
      image1:(restaurant.yelp_photos == null) ? '' : restaurant.yelp_photos[0], // TODO: possibly get google image instead
      price:restaurant.yelp_price,
      description:'Farm-fresh Québécois dishes & tasting menus from renowned chef Normand Laprise, plus fine wines.',
      website:restaurant.website
    });
  }

  render() {
    return (
      <div>
        <Gmap changeCard={this.changeCard.bind(this)}/>
        <CardCustom 
          restaurantName={this.state.restaurantName} 
          image1={this.state.image1} 
          price={this.state.price} 
          description={this.state.description}
          website={this.state.website}/>
      </div>
    );
  }
}

export default App;


