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
		window.lat = position.coords.latitude;
		window.lon = position.coords.longitude;
		var center = new google.maps.LatLng(window.lat, window.lon)
		map.panTo( center );
		map.setZoom(10);
	} else {
		get_location();
	}
}

function warning_level(lat, lon){
	var request = new XMLHttpRequest();
	url = '/warning_level?lon='+lon+'&lat='+lat;

	request.onreadystatechange = function() {
	if (request.readyState == 4 && request.status == 200){
			var level = request.responseText;
			console.log(level);
		}
	}
	request.open("GET", url, true); // true for asynchronous
	request.send(null);
}

update();
