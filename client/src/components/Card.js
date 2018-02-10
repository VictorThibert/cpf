import React from 'react';

class Card extends React.Component {

	constructor() {
		super();
		this.test='HelloWorld';
	}

	render() {
		const style = {
			position:'absolute',
			top: '80px',
			right: '50px',
		};

		return (
			<div style={style}>
				<h2> {this.props.text} </h2>
			</div>
		)
	}

}

export default Card