// reduce store
// any file that imports this gets the same store

import { applyMiddleware, compose, createStore } from 'redux';

import { createLogger } from 'redux-logger';
import thunk from 'redux-thunk';
import reducer from './reducers'; // imports that index.js

const middleWare = applyMiddleware(thunk, createLogger());

// dev tool enable
const enhancers = compose(
	window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);

const store = createStore(reducer, enhancers, middleWare);

export default store 

