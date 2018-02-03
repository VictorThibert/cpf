import React from 'react';
import { connect } from 'react-redux';
import List from './List';

const Board = () => (
    <div className="project-board">
        <List status="LIST"> 
            Restaurants
        </List>
    </div>
);

export default Board;