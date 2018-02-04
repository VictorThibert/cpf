import React from 'react';

function RestaurantList(props){
    console.log("RestaurantList",props._id,"text",props.text);
    return (
        <div className="project-card" onClick={() => props.onChangeClick(props._id)}>
            <p className="card-text">{props.name}</p> 
            <span className="card-executor">{props.executor}</span> 
            <span>{props.cost}</span>
        </div>
    );
}

export default RestaurantList;