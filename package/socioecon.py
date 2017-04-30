import requests
import json
from unidecode import unidecode
from pprint import pprint

def poverty_level( lat, lon ):
	params = {
    	'lat':str(lat),
    	'lng':str(lon),
    	'username':'me'
	}
	url = 'http://ws.geonames.org/countryCodeJSON'
	response = requests.get(url,params=params)
	data = response.json()
	country = data['countryName']
	level = COUNTRIES.get(country,0)
	return str(level)


COUNTRIES = {
    'Austria': 0.092825,
    'Belgium': 0.10615,
    'Canada': 0.118531,
    'Switzerland': 0.10425,
    'Chile': 0.18,
    'Czechia': 0.060275,
    'Germany': 0.088063,
    'Denmark': 0.049583,
    'Spain': 0.156375,
    'Estonia': 0.137625,
    'Finland': 0.062652,
    'France': 0.079125,
    'United Kingdom': 0.127167,
    'Greece': 0.1404,
    'Hungary': 0.10325,
    'Ireland': 0.1069,
    'Iceland': 0.0606,
    'Israel': 0.199875,
    'Italy': 0.132575,
    'Japan': 0.16425,
    'South Korea': 0.203,
    'Lithuania': 0.141775,
    'Luxembourg': 0.078125,
    'Russia': 0.160025,
    'Mexico': 0.2005,
    'Netherlands': 0.07015,
    'Norway': 0.069393,
    'New Zealand': 0.1015,
    'Poland': 0.107444,
    'Portugal': 0.129675,
    'Slovakia': 0.08075,
    'Slovenia': 0.09645,
    'Sweden': 0.09075,
    'Turkey': 0.0190417,
    'United States': 0.185,
}

if __name__=='__main__':
    pass
