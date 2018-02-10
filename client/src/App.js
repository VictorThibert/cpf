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
      image: '',
      price:''
    }
  }

  changeCard(restaurant) {
    this.setState({
      restaurantName:restaurant.name,
      image:restaurant.yelp_photos[0],
      price:restaurant.yelp_price_level

    });
  }

  render() {
    return (
      <div>
        <Gmap changeCard={this.changeCard.bind(this)} text={this.state.restaurantName}/>
        <CardCustom restaurantName={this.state.restaurantName} image={this.state.image} price={this.state.price}/>
      </div>
    );
  }
}

export default App;


