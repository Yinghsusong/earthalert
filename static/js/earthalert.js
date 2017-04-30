
function get_location(){
	if( navigator.geolocation ){
		navigator.geolocation.getCurrentPosition( function( position ){
			window.lat = position.coords.latitude;
			window.lon = position.coords.longitude;
			console.log(window.lat);
			console.log(window.lon);
		}, decline_pos, {timeout:10000});
	} else {
		alert( 'You won\'t be able to submit reports.' );
	}
}

function decline_pos( error ){
	console.log( error );
	alert( 'There was a problem getting your location- you won\'t be able to submit reports.' );
}

function update( position ){
	if(position){
		window.lat = position.coords.latitude;
		window.lon = position.coords.longitude;
		var center = new google.maps.LatLng(window.lat, window.lon)
		var marker = new google.maps.Marker({
          position: {lat: window.lat, lng:window.lon},
          map: map
        });
		map.panTo( center );
		map.setZoom(10);
		warning_level(lat,lon);

		window.latitude = lat;
		window.longitude = lon;

		console.log(window.latitude);
		console.log(window.longitude);
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
			window.warning_level = level;
			console.log(window.warning_level);
		}
	}
	request.open("GET", url, true); // true for asynchronous
	request.send(null);
}

update();
