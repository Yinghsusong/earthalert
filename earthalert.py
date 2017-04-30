# ------------------------------------------------------------------------------
# outside imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, render_template, make_response
import json
import os

from twilio.twiml import messaging_response

# local imports
from package import models
from package.utilities import *

# initial setup
db_engine = create_engine( 'sqlite:///earthalert.db' )
session_generator = sessionmaker(bind=db_engine)
session = session_generator()

LOCATION = os.path.dirname(os.path.abspath(__file__))

# init the app
app = Flask(__name__)
app.debug = True

# this is the index page. Going to http://localhost:5000/ when the
@app.route("/")
# project is running will bring you here
def index():
	events = [ e.json() for e in session.query( models.Event ).all() ]
	images = [ e.json() for e in session.query( models.Image ).all() if e.path ]

	log = open('LOG.txt','a')
	log.write(str(len(images)))

	url = get_geo_url()
	return render_template( 'index.html', geo_url=url, events=events, images=images )

@app.route("/report", methods=['GET'])
def report():
	desc = request.values.get('desc')
	lat = request.values.get('lat')
	lon = request.values.get('lon')
	event = models.Event( lat, lon, desc )
	try:
		session.add( event )
		session.commit()
		return 'GOOD'
	except Exception as e:
		session.rollback()
		print(e)
		return 'BAD'

@app.route("/upload", methods=['POST'])
def upload():
	try:
		lon = request.values.get('lon')
		lat = request.values.get('lat')
		f = request.files['file']

		partial = 'static/upload/{}'.format(f.filename)

		path = os.path.join(LOCATION,partial)
		f.save(path)

		image = models.Image( lat, lon, '/' + partial )

		try:
			session.add(image)
			session.commit()
		except:
			session.rollback()
			raise
	except Exception as e:
		print(e)
	return ''


@app.route("/notify_me", methods=[ 'GET', 'POST'])
def notify_me():
	number =''
	if request.method == "POST":
		number = request.values.get('number')
		lat = request.values.get('lat', None)
		lon = request.values.get('lon', None)
		if number:
			person = models.Person()
			person.set( lat, lon, number )
			try:
				session.add( person )
				session.commit()

			except:
				session.rollback()
				try:
					person = session.query(Person).filter(Person.phone==number).first()
					person.set( number, lat, lon )
					session.commit()
				except:
					pass
		return render_template( 'report.html' )
	else:
		return render_template( 'report.html')

@app.route("/fetch", methods=['GET'])
def fetch():
	lat = request.values.get('lat')
	lon = request.values.get('lon')
	if lat and lon:
		return get_geo_json( lat, lon )
	else:
		return get_geo_json()

@app.route("/sms", methods=['GET'])
def sms_reply():
	log = open('LOG','a')
	try:
		number = request.values.get('From','FROM_NOT_FOUND')
		message_body = request.values.get('Body','BODY_NOT_FOUND')

		country = request.values.get('FromCountry','')
		state = request.values.get('FromState','')
		city = request.values.get('FromCity','')

		log.write(country +'\n')
		log.write(state +'\n')
		log.write(city +'\n')

		location = [ l.strip() for l in message_body.split(',') if l ]
		if len(location)==2 and isfloat( location[0] ) and isfloat( location[1] ):
			lat = location[0]
			lon = location[1]
		else:
			lat, lon = get_long_lat( country, state, city )

		log.write(str(lat) +'\n')
		log.write(str(lon) +'\n')

		danger_level = alert_level( lat, lon )
		level = alert_level_str( danger_level )

		log.write(str(danger_level) + '\n')
		log.write(str(level) + '\n')

		response = messaging_response.MessagingResponse()
		response.message('Your risk level is: {} ({})'.format(level,danger_level),to=number,from_='2563611265')
		log.write(response.to_xml() + '\n')
		return response.to_xml()
	except Exception as e:
		log.write(str(type(e)) + ': ' + str(e) + '\n')


@app.route("/warning_level", methods=['GET'])
def warning_level():
	lat = request.values.get('lat')
	lon = request.values.get('lon')
	level = alert_level(lat,lon)
	return str(level)

if __name__ == "__main__":
	app.debug = True
	app.run()
