import React, { Component } from 'react';

import Gmap from './Components/Gmap';
import CardCustom from './Components/CardCustom.js';

import 'semantic-ui-css/semantic.min.css';




class App extends Component {

  constructor() {
    super();
    this.state = {
      restaurantName: 'R1',
      image: '' // default image
    }
  }

  changeCard(restaurant) {
    this.setState({
      restaurantName:restaurant.name,
      image:restaurant.yelp_photos[0]
    });
  }

  render() {
    return (
      <div>
        <Gmap changeCard={this.changeCard.bind(this)} text={this.state.restaurantName}/>
        <CardCustom restaurantName={this.state.restaurantName} image={this.state.image}/>
      </div>
    );
  }
}

export default App;


