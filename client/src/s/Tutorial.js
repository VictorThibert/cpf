// default state
const defaultState = {
  welcome: 'Hello default', // properties
  otherState: 'Some stuff'
};

// reducer
const greeting = (state = defaultState, action) => {
  switch(action.type) {
    case 'GREET_ME':
      return { ...state, welcome:`Welcome ${action.name}`}; // the past state but override welcome
    case 'GREET_WORLD':
      return { ...state, welcome:'Hello world'};
    default:
      return state // initially coming in state
  } 
}; 

// create data/state store
const store = createStore(greeting);// accepts a function as input

console.log(store.getState());


// sends an action of this type
store.dispatch({
  type: 'GREET_ME',
  result: 'result' // same syntax (kinda annoying)
});

console.log(store.getState());






/////////////////////////
const defaultState2 = {};
const reducer2 = (state = defaultState2, action) => {
  switch (action.type) {
    case "FETCH_DATA": {
      break;
    }
    case "RECEIVE_USERS": {
      break;
    }
    default:
      break;
  }
  return state
}
const middleWare2 = applyMiddleware(thunk, createLogger());
const store2 = createStore(reducer2, middleWare2);

store2.dispatch((dispatcher_function) => {
  dispatcher_function({type:"FETCH_DATA"});
  axios.get("http://cherrypicker.io:4000/restaurant/get_list?limit=10")
    .then((response) => {
      dispatcher_function({type:"RECEIVE_USERS", payload: response.data})
    });
  // do something async
})