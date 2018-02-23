import React, { Component } from 'react';

import Gmap from './components/Gmap';
import CardCustom from './components/CardCustom.js';
import 'semantic-ui-css/semantic.min.css';
import bannerImage from './images/montreal.png';

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
      center: {
        lat:45.5,
        lng:-73.5
      },
      defaultCenter: {
        lat:45.5,
        lng:-73.5
      },
      city: 'montreal',
      isVisible: false,
      bannerImage: bannerImage,
    }
  }

  changeCard(restaurant, coordinates) {
    this.setState({
      restaurantName:restaurant.name,
      image1:(restaurant.yelp_photos == null) ? '' : restaurant.yelp_photos[0], // TODO: possibly get google image instead (or use different than 1st (e.g. random))
      price:restaurant.yelp_price,
      description:'Farm-fresh Québécois dishes & tasting menus from renowned chef Normand Laprise, plus fine wines.',
      website:restaurant.website,
      center: coordinates,
      isVisible: true,
      bannerImage: bannerImage,
    });
  }

  render() {
    return (
      <div>
        <Gmap 
          changeCard={this.changeCard.bind(this)} 
          center={this.state.center}
          defaultCenter={this.state.defaultCenter}
          fetchLimit={10}
        />
        <CardCustom 
          restaurantName={this.state.restaurantName} 
          image1={this.state.image1} 
          price={this.state.price} 
          description={this.state.description}
          website={this.state.website}
          isVisible={this.state.isVisible}
          bannerImage={this.state.bannerImage}
        />
      </div>
    );
  }
}

export default App;


