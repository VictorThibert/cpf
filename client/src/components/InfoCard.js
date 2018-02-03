import React from 'react';

function InfoCard (props){
    return (
        <div className="project-card" >
        <div onClick={() => props.onChangeClick()}> {'<Back'}</div>
            <p className="card-text">{props.restaurantInfo[0].image}</p> 
            <span className="card-executor">{props.restaurantInfo[0].executor}</span> 
            <span>This place costs {props.restaurantInfo[0].cost}</span>
        </div>
    );
};

export default InfoCard;