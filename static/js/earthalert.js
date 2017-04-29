

function get_location(){
	if( navigator.geolocation ){
		navigator.geolocation.getCurrentPosition( update_pos, decline_pos );
	} else {
		alert( 'You won\'t be able to submit reports.' );
	}
}

function update_pos( position ){
	document.getElementById('lat').setAttribute('value',position.coords.latitude);
	document.getElementById('lon').setAttribute('value',position.coords.longitude);
}

function decline_pos( error ){
	alert( 'There was a problem getting your location- you won\'t be able to submit reports.' );
}

get_location();
