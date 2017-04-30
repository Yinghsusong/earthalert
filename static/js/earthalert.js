
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

// Get the modal
var modal = document.getElementById('myModal');

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

update();
