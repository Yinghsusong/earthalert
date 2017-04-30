
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
            '<p><b>Refer to box at upper right for your current threat level</b></p>'
            '</div>'+
            '</div>';

        var infowindow = new google.maps.InfoWindow({
        	content: contentString
        });
        var image = '/static/img/home.png'
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
		init_events();

		window.lat = lat;
		window.lon = lon;

		warning_level(lat,lon);
	} else {
		get_location();
	}
}

function calculate_warning_level( base ){
	//for(var i=0;i<EVENTS.length;i++){
	//	console.log( EVENTS[i] );
	//}
	//return base;
}

function warning_level(lat, lon){
	var box = document.getElementById('warning_box');
	box.innerHTML = 'Fetching Risk Level . . .';
	var request = new XMLHttpRequest();
	url = '/warning_level?lon='+lon+'&lat='+lat;

	request.onreadystatechange = function() {
	if (request.readyState == 4 && request.status == 200){
			var warning_level = calculate_warning_level( parseInt(request.responseText) );
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

function report_event(){
	var desc = window.prompt("You are reporting a landslide event in your area. Please provide a short description.","");
	var lat = window.lat;
	var lon = window.lon;
	if(lon&&lat){
		var request = new XMLHttpRequest();
		url = '/report?lon='+lon+'&lat='+lat+'&desc='+desc;
		request.onreadystatechange = function() {
			if (request.readyState == 4 && request.status == 200){
			}
		}
		request.open("GET", url, true); // true for asynchronous
		request.send(null);
	}
}

function get_file(){
	var fileobj = document.getElementById('file_input');
	fileobj.addEventListener('change',function(){
		for(var i=0; i<this.files.length;i++){
			var file = this.files[i];
			file_upload( file );
		}
	})
	fileobj.click();
}

function file_upload( file ){
	var lat = window.lat;
	var lon = window.lon;

	var url = '/upload';
	var xhr = new XMLHttpRequest();
	var fd = new FormData();
	xhr.open("POST", url, true);

	fd.append("file", file);
	fd.append("lat", lat);
	fd.append("lon", lon);


	xhr.send(fd);
}
