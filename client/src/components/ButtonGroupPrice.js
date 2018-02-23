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
    console.log(currentButtonToggles)
    this.setState({
      buttonToggles: currentButtonToggles
    })

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
