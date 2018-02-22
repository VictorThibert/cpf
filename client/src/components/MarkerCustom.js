/* eslint-disable no-undef */
// this above line is critical, do not remove 

import React from 'react';
import { Marker } from 'react-google-maps';

class MarkerCustom extends React.Component {
    constructor() {
        super();

        this.state = {
            icon: {
                url: 'https://i.cubeupload.com/ThtjvX.png',
                scaledSize: new google.maps.Size(198/6, 281/6)
            },
        }
    }

    onMouseOver() {
        const scaleFactor = this.props.scaleFactor - 1
        const largeIcon = {
            url: this.props.icon.url,
            scaledSize: new google.maps.Size(198/scaleFactor, 281/scaleFactor)
        }
        this.setState({icon:largeIcon})
    }

    onMouseOut() {
        this.setState({icon:this.props.icon})
    }

    componentWillMount() {
        this.setState({icon:this.props.icon})
    }


    render() {
        return (
            <Marker 
                position = {this.props.position}
                key = {this.props.restaurantId}
                onClick = {this.props.onClick}
                icon = {this.state.icon}
                onMouseOver = {this.onMouseOver.bind(this)}
                onMouseOut = {this.onMouseOut.bind(this)}
                animation = {null}
            />
        )
    }
}

export default MarkerCustom;