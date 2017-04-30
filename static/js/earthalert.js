
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
		var contentString = '<div id="content">'+
            '<div id="siteNotice">'+
            '</div>'+
            '<h1 id="firstHeading" class="firstHeading">Your Position</h1>'+
            '<div id="bodyContent">'+
            '<p><b>Refer to box at upper right for your current threat level</b></p>'+ <p> 
            '</div>'+
            '</div>';

        var infowindow = new google.maps.InfoWindow({
        	content: contentString
        });

		var marker = new google.maps.Marker({
          position: {lat: lat, lng:lon},
          title: 'Your Position',
          map: map
        });
        marker.addListener('click', function(){
        	infowindow.open(map, marker);
        });
		map.panTo( center );
		map.setZoom(10);

		window.lat = lat;
		window.lon = lon;

		warning_level(lat,lon);
	} else {
		get_location();
	}
}

function warning_level(lat, lon){
	var box = document.getElementById('warning_box');
	box.innerHTML = 'Fetching Risk Level . . .';
	var request = new XMLHttpRequest();
	url = '/warning_level?lon='+lon+'&lat='+lat;

	request.onreadystatechange = function() {
	if (request.readyState == 4 && request.status == 200){
			var warning_level = parseInt(request.responseText);
			switch(warning_level){
				case 0:
					box.classList.add('low');
					box.innerHTML = 'Low risk in your area';
					break;
				case 1:
					box.classList.add('med');
					box.innerHTML = 'Medium risk in your area';
					break;
				case 2:
					box.classList.add('high');
					box.innerHTML = 'High risk in your area';
					break;
				default:
					box.classList.add('unkn');
					box.innerHTML = 'Unknown risk in your area';
					break;
			}
		}
	}
	request.open("GET", url, true); // true for asynchronous
	request.send(null);
}

update();

function report_event(){
	var description = window.prompt("You are reporting a landslide event in your area. Please provide a short description.","");
	if(description){
		console.log(window.lat);
		console.log(window.lon);
	}
}
