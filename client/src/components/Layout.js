import React from 'react';

class Layout extends React.Component {
	constructor() {
		super();
		this.name = 'Layout';
	}

	handleChange(e) {
		const title = e.target.value;
		this.props.changeT(title);
	}

	render() {

		return (
			<div>
				<h2> {this.name} and {this.props.text} </h2>
				<input onChange={this.handleChange.bind(this)}/>
			</div>
		);
	}
}

export default Layout