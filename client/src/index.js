import React from 'react';
import { render } from 'react-dom';
import { createStore, applyMiddleware } from 'redux';
import promiseMiddleware from 'redux-promise-middleware';
import thunkMiddleware from 'redux-thunk';
import { Provider } from 'react-redux';
import restaurants from './reducers';
import App from './components/App';
import initialData from '../data';

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(restaurants, initialData, composeEnhancers(
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