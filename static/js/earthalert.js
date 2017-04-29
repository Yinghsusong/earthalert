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
		map.setZoom(10);
	} else {
		get_location();
	}
}

function get_geojson( lon, lat ){
	var request = new XMLHttpRequest();
	url = '/fetch?lon='+lon+'&lat='+lat;

	request.onreadystatechange = function() {
		if (request.readyState == 4 && request.status == 200){
			map.data.loadGeoJson(request.responseText);
		}
	}
	request.open("GET", url, true); // true for asynchronous
	request.send(null);
}

update();
