
function get_location(){
	if( navigator.geolocation ){
		navigator.geolocation.getCurrentPosition( update, error );
	} else {
		alert( 'You won\'t be able to submit reports.' );
	}
}

function error( e ){
	console.log( e );
	alert( 'There was a problem getting your location- you won\'t be able to submit reports.' );
}

function update( position ){
	if(position){
		var lat = position.coords.latitude;
		var lon = position.coords.longitude;
		var center = new google.maps.LatLng( lat, lon)
		var marker = new google.maps.Marker({
          position: {lat: lat, lng:lon},
          map: map
        });
		map.panTo( center );
		map.setZoom(10);
		warning_level(lat,lon);
	} else {
		get_location();
	}
}

function warning_level(lat, lon){
	var request = new XMLHttpRequest();
	url = '/warning_level?lon='+lon+'&lat='+lat;

	request.onreadystatechange = function() {
	if (request.readyState == 4 && request.status == 200){
			var warning_level = parseInt(request.responseText);
			var box = document.getElementById('warning_box');
			switch(warning_level){
				case 0:
					box.classList.add('low');
					break;
				case 1:
					box.classList.add('med');
					break;
				case 2:
					box.classList.add('high');
					break;
				default:
					box.classList.add('unkn');
					break;
			}
		}
	}
	request.open("GET", url, true); // true for asynchronous
	request.send(null);
}

update();
