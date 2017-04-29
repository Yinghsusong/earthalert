var userLon;
var userLat;

function get_location(){
	if( navigator.geolocation ){
		navigator.geolocation.getCurrentPosition( update, decline_pos );
	} else {
		alert( 'You won\'t be able to submit reports.' );
	}
}

function decline_pos( error ){
	alert( 'There was a problem getting your location- you won\'t be able to submit reports.' );
}

function update( position ){
	if(position){
		lat = position.coords.latitude;
		lon = position.coords.longitude;
		var center = new google.maps.LatLng(lat, lon)
		map.panTo( center );
	} else {
		get_location();
	}
}

update();
