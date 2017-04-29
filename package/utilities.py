from datetime import datetime

def get_datetime_str():
	return datetime.now().strftime('%Y-%m-%d')

def get_geo_json(timeStamp, lat=0, lon=0):
	base_url = 'https://pmmpublisher.pps.eosdis.nasa.gov/opensearch?q=global_landslide_nowcast_30mn'
	lat_value = 'lat=' + str(lat)
	lon_value = 'lon=' + str(lon)
	limit = 'limit=1'
	startTime = 'startTime=' + str(timeStamp)
	endTime = 'endTime=' + str(timeStamp)
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

	geo_json = requests.get(geo_url).json()									
	#legend = requests.get(legend_url).json()
	color_table = requests.get(color_url).json()		
	return geo_json
