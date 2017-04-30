from datetime import datetime, timedelta
import requests
from pprint import pprint
import json
from shapely.geometry import shape, Point

def get_datetime_str( days_behind=0 ):
	date = datetime.now() - timedelta(days=days_behind)
	return date.strftime('%Y-%m-%d')

def get_geo_json( lat=0, lon=0 ):
	url = get_geo_url( lat, lon )
	return requests.get(url).text

def get_geo_url( lat=0, lon=0 ):
	base_url = 'https://pmmpublisher.pps.eosdis.nasa.gov/opensearch?q=global_landslide_nowcast_30mn'
	lat_value = 'lat=' + str(lat)
	lon_value = 'lon=' + str(lon)
	limit = 'limit=1'
	startTime = 'startTime=' + get_datetime_str(1)
	endTime = 'endTime=' + get_datetime_str()
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
	return geo_url

def get_polygons( lat, lon ):
	dt = datetime.now().strftime('%Y-%m-%d')
	url = 'https://pmmpublisher.pps.eosdis.nasa.gov/opensearch'
	params = {
		'q':'global_landslide_nowcast_30mn',
		'lat':str(lat),
		'lon':str(lon),
		'limit':1,
		'startTime':dt,
		'endTime':dt
	}
	data = requests.get( url, params=params ).json()
	geojson = None
	for action in data['items'][0]['action']:
		for item in action['using']:
			if item['@id']=='geojson':
				geojson = item['url']

	if geojson:
		geo_data = requests.get(geojson)
		pprint( geo_data )

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
