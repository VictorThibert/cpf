import React from 'react';
import { Card, Icon, Image /*, Reveal */ } from 'semantic-ui-react';

const style = {
        position:'absolute',
        top: '50px',
        right: '60px',
        boxShadow: '0 1px 4px 0px #0000002e, 0 0 0 0px #708490',
};


class CardCustom extends React.Component {
    render() {


        let extra;
        if (this.props.website !== ''){
            extra = (
              <a href={this.props.website}>
                <Icon name='food'/>
                Website
              </a>
            )
        } 


        const image = ( 
            //<Reveal animated='move'>
            //    <Reveal.Content visible>
            //        <Image src={this.props.image1}/>
            //    </Reveal.Content>
            //    <Reveal.Content hidden>
            //     <Image src={this.props.image2}/>
            //    </Reveal.Content>
            //</Reveal>
            <Image src={this.props.image1}/>
        )
            

        return (
            <Card
                image={image}
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

//  constructor() {
//      super();
//      this.test='HelloWorld';
//  }

//  render() {
//      const style = {
//          position:'absolute',
//          top: '80px',
//          right: '50px',
//      };

//      return (
//          <div style={style}>
//              <h2> {this.props.text} </h2>
//          </div>
//      )
//  }

// }

// export default Card