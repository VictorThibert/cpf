import React from 'react';
import { Button } from 'semantic-ui-react';

const groupStyle = {
    position:'absolute',
    bottom: '50px',
    right: '60px',
    boxShadow: '0 0px 3px 0px #0000002e, 0 0 0 0px #708490',
    background: 'white',
    border: 'none',
    width: '270px',
};

const buttonStyle = {
  border: 'none',

}



class ButtonGroupPrice extends React.Component {

  constructor() {
    super();
    this.state = {
      buttonToggles: {
        $:true,
        $$:true,
        $$$:true,
        $$$$:true,
      }
    }
  }

  buttonPress(event, data) {
    const changedButton = data.content;
    let currentButtonToggles = this.state.buttonToggles;
    currentButtonToggles[changedButton] = !currentButtonToggles[changedButton];
    this.setState({
      buttonToggles: currentButtonToggles
    })

    // call App.js to rerender pins

    const price1 = currentButtonToggles['$'] ? '$' : '';
    const price2 = currentButtonToggles['$$'] ? '$$' : '';
    const price3 = currentButtonToggles['$$$'] ? '$$$' : '';
    const price4 = currentButtonToggles['$$$$'] ? '$$$$' : '';
    const prices = [price1, price2, price3, price4];

    const priceLevelString = prices.join(',');

    this.props.buttonPress(priceLevelString);
  }

  render() {
    return (
      <Button.Group basic style={groupStyle}>
        <Button 
          toggle active={this.state.buttonToggles.$}
          style={buttonStyle}
          onClick={this.buttonPress.bind(this)}
          content='$'
        />
        <Button 
          toggle active={this.state.buttonToggles.$$}
          style={buttonStyle}
          onClick={this.buttonPress.bind(this)}
          content='$$'
        />
        <Button 
          toggle active={this.state.buttonToggles.$$$}
          style={buttonStyle}
          onClick={this.buttonPress.bind(this)}
          content='$$$'
        />
        <Button 
          toggle active={this.state.buttonToggles.$$$$}
          style={buttonStyle}
          onClick={this.buttonPress.bind(this)}
          content='$$$$'
        />
      </Button.Group>
    )
  }
}

export default ButtonGroupPrice
