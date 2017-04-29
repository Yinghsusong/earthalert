from datetime import datetime
import requests
from pprint import pprint

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


if __name__=='__main__':
	pass
