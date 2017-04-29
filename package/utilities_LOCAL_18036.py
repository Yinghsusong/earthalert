from datetime import datetime
import requests
import json
from shapely.geometry import shape, Point

def get_datetime_str():
	return datetime.now().strftime('%Y-%m-%d')

def get_geo_json( lat=0, lon=0):
	base_url = 'https://pmmpublisher.pps.eosdis.nasa.gov/opensearch?q=global_landslide_nowcast_30mn'
	lat_value = 'lat=' + str(lat)
	lon_value = 'lon=' + str(lon)
	limit = 'limit=1'
	startTime = 'startTime=' + str(get_datetime_str())
	endTime = 'endTime=' + str(get_datetime_str())
	url = '&'.join([base_url, lat_value, lon_value, limit, startTime, endTime])
	results = requests.get(url)
	json_data = results.json()
	for key,value in json_data.items():
		if key == 'items':
			for elem in value:
				for key,value in elem.items():
					if key == 'action':
						for elem in value:
							for key, value in elem.items():
								if key=='using':
									for elem in value:
										data_dict = elem
										for key,value in elem.items():
											if key == '@id' and value == 'geojson':
												geo_url = (data_dict['url'])

											if key == '@id' and value =='legend':
												legend_url = data_dict['url']
											if key == '@id' and value == 'style':
												color_url = data_dict['url']

	geo_json = requests.get(geo_url).text
	#legend = requests.get(legend_url).json()
	color_table = requests.get(color_url).text
	return geo_json

def alert_level(lat, lon):
	# load GeoJSON file containing sectors
	geo_json=get_geo_json()
	danger_level = 0
	js = json.loads(geo_json)
	#with open(geo_json) as f:
	 #   js = json.load(f)

	# construct point based on lon/lat returned by geocoder
	point = Point(float(lat), float(lon))

	# check each polygon to see if it contains the point
	for feature in js['features']:
	    polygon = shape(feature['geometry'])
	    center = polygon.centroid
	    if polygon.contains(point):
	        # print('Found containing polygon:', feature)
	        danger_level = feature['properties']['nowcast']

	return str(danger_level)


