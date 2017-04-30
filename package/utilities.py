from datetime import datetime, timedelta
import requests
from pprint import pprint
import json
import matplotlib.path as matpath
import numpy as np
from package.socioecon import poverty_level
from geocodio import GeocodioClient

def get_long_lat( country, state, city ):
	client = GeocodioClient('05047884974545850d50078551d55d49cd80905')
	location = data = client.geocode('{}, {} {}'.format(city,state,country))['results'][0]['location']
	lat = location['lat']
	lon = location['lng']
	return lat, lon

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

def alert_level(lat, lon):
	# load GeoJSON file containing sectors
	geo_json=get_geo_json()
	js = json.loads(geo_json)

	rating = float( poverty_level( lat, lon ) )

	# check each polygon to see if it contains the point
	for feature in js['features']:
		poly = feature['geometry']['coordinates'][0]
		path = matpath.Path(np.array(poly))
		inside = path.contains_point((float(lat),float(lon)))
		if inside:
			nowcast = float(feature['properties']['nowcast'])
			return str(nowcast+rating)
	return str(0+rating)

def alert_level_str( level ):
	level = int(level)
	if level<0:
		return 'Uknown'
	elif 0 <= level < 1:
		return 'Low'
	elif 1 <= level < 2:
		return 'Medium'
	elif 2 <= level < 3:
		return 'High'
	else:
		return 'Extreme'
