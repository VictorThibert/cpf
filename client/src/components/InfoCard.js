import React from 'react';

function InfoCard (props){
    return (
        <div className="project-card" >
        <div onClick={() => props.onChangeClick()}> {'<Back'}</div>
        <h2>{props.restaurantInfo[0].name}</h2>
        <img style={{ width: 70, height: 61 }} src={props.restaurantInfo[0].yelp_photos[0]||"../static/placeholder.png"} />
        </div>
    );
};

export default InfoCard;