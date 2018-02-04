import React from 'react';
import { render } from 'react-dom';
import { createStore, applyMiddleware, compose } from 'redux';
import promiseMiddleware from 'redux-promise-middleware';
import thunkMiddleware from 'redux-thunk';
import { Provider } from 'react-redux';
import restaurants from './reducers';
import App from './components/App';
import {initialData,getRestaurantList} from './utils/FetchData';
import data from '../data/index'


const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(restaurants, data, composeEnhancers(
    applyMiddleware(
        thunkMiddleware,
        promiseMiddleware()
    )
));


render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('app')
);



export default store;