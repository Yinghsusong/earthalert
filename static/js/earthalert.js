// -----------------------------------------------------------------------------
// FUNCTIONS

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
        var image = '/static/img/home.png';

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
		//init_events();

		window.lat = lat;
		window.lon = lon;

		warning_level(lat,lon);
	} else {
		get_location();
	}
}

function calculate_warning_level( base, lat, lon ){
	var base = parseFloat( base );
	var lat = parseFloat( lat );
	var lon = parseFloat( lon );
	for(var i=0;i<EVENTS.length;i++){
		item = EVENTS[i];
		diff = {
			'x': Math.abs( parseFloat(item.latitude) ) - Math.abs( lat ),
			'y': Math.abs( parseFloat(item.longitude) ) - Math.abs( lon ),
		}
		if(diff.x<0.5&&diff.y<0.5){
			base += 0.1;
		}
	}
	return base;
}

function warning_level(lat, lon){
	var box = document.getElementById('warning_box');
	box.innerHTML = 'Fetching Risk Level . . .';
	var request = new XMLHttpRequest();
	url = '/warning_level?lon='+lon+'&lat='+lat;

	request.onreadystatechange = function() {
	if (request.readyState == 4 && request.status == 200){
			var wl = calculate_warning_level( request.responseText, lat, lon );
			if( wl >= 0 && wl < 1){
				box.classList.add('low');
				box.innerHTML = 'Low risk in your area';
			}
			else if( wl >= 1 && wl < 2){
				box.classList.add('med');
				box.innerHTML = 'Medium risk in your area';
			}
			else if( wl >= 2 && wl < 3 ){
				box.classList.add('high');
				box.innerHTML = 'High risk in your area';
			}
			else if( wl >= 3 ){
				box.classList.add('high');
				box.innerHTML = 'Extreme risk in your area';
			}
			else{
				box.classList.add('unkn');
				box.innerHTML = 'Unknown risk in your area';
			}
		}
	}
	request.open("GET", url, true); // true for asynchronous
	request.send(null);
}

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

function information(){
	 var check = window.alert("SLIDE, or Suspected Landslide Identification Environment, is aresponsive web app designed by Team EarthAlert to help save lives utilizing data collected from NASA’s observation satellites and their NowCast system. As well, the community can contribute their own landslide data to a data base operated by team EarthAlert to improve the global understanding of how and where landslides strike.");
}

// -----------------------------------------------------------------------------
// code runs on import

//Modal Updated Functions
$("#upload").on('click' , function(e) {
    e.preventDefault();
    $("#imageUploadContainer").toggleClass("displayBlock");
});

$("#report").on('click' , function(e) {
    e.preventDefault();
    $("#editReportContainer").toggleClass("displayBlock");
});

$("#info").on('click' , function(e) {
    e.preventDefault();
    $("#infoContainer").toggleClass("displayBlock");
});


update();


