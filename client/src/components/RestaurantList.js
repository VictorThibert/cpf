import React from 'react';

function RestaurantList(props){
    console.log("RestaurantList",props.id,"text",props.text);
    return (
        <div className="project-card" onClick={() => props.onChangeClick(props.id)}>
            <p className="card-text">{props.text}</p> 
            <span className="card-executor">{props.executor}</span> 
            <span>{props.cost}</span>
        </div>
    );
}

export default RestaurantList;