import React from 'react';
import { Card, Icon, Image } from 'semantic-ui-react';

const style = {
		position:'absolute',
		top: '50px',
		right: '60px',
	};



class CardCustom extends React.Component {
	render() {

		
		let extra;
		if (this.props.website != ''){
			extra = (
			  <a href={this.props.website}>
			    <Icon name='food'/>
			    Website
			  </a>
			)
		} else {
			extra = ''
		}
			

		return (
			<Card
				image={this.props.image}
				style={style}
				header={this.props.restaurantName}
				meta={this.props.price}
				description={this.props.description}
				extra={extra}
			/> 
		)
	}
}

export default CardCustom

// import React from 'react';

// class Card extends React.Component {

// 	constructor() {
// 		super();
// 		this.test='HelloWorld';
// 	}

// 	render() {
// 		const style = {
// 			position:'absolute',
// 			top: '80px',
// 			right: '50px',
// 		};

// 		return (
// 			<div style={style}>
// 				<h2> {this.props.text} </h2>
// 			</div>
// 		)
// 	}

// }

// export default Card