import React from 'react';
import { Card, Icon, Image } from 'semantic-ui-react';

const style = {
		position:'absolute',
		top: '50px',
		right: '60px',
	};

const extra = (
  <a>
    <Icon name='user' />
    16 Friends
  </a>
)

class CardExampleCard extends React.Component {
	render() {
		return (
			<Card
				image={this.props.image}
				style={style}
				header={this.props.restaurantName}
				meta='Friend'
				description='Elliot is a sound engineer living in Nashville who enjoys playing guitar and hanging with his cat.'
				extra={extra}
			/> 
		)
	}
}

export default CardExampleCard

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