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
      price:'',
      description:'',
      website:''
    }
  }

  changeCard(restaurant) {
    this.setState({
      restaurantName:restaurant.name,
      image:restaurant.yelp_photos[0],
      price:restaurant.yelp_price,
      description:'Farm-fresh Québécois dishes & tasting menus from renowned chef Normand Laprise, plus fine wines.',
      website:restaurant.website
    });
  }

  render() {
    return (
      <div>
        <Gmap changeCard={this.changeCard.bind(this)} text={this.state.restaurantName}/>
        <CardCustom 
          restaurantName={this.state.restaurantName} 
          image={this.state.image} 
          price={this.state.price} 
          description={this.state.description}
          website={this.state.website}/>
      </div>
    );
  }
}

export default App;


