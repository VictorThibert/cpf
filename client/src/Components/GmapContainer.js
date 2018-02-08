import { connect } from 'react-redux';
import { fetchData, fetchDataSuccess } from '../Actions/testActions.js';
import Gmap from './Gmap.js'

const mapStateToProps = (state) => {
	return {
		data: state.data
	};
}


const mapDispatchToProps = (dispatch) => {
	return {
		fetchData: () => {
			dispatch(fetchData()).then((response) => {
				dispatch(fetchDataSuccess(response.payload.data));
			})
		}
	}
}


export default connect(mapStateToProps, mapDispatchToProps)(Gmap);