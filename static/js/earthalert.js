// GLOBALS
var userLon = null;
var userLat = null;


function get_location(){
	if( navigator.geolocation ){
		navigator.geolocation.getCurrentPosition( printposition, errorposition );
	} else {
		alert( 'Your experience may be negatively impacted because your browser doesn\'t support location services.' );
	}
}

function printposition( position ){
	userLon = position.coords.longitude;
	userLat = position.coords.latitude;
}

function errorposition( error ){
	alert( 'There was a problem getting your location' );
}

get_location();
