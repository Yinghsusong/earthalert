# ------------------------------------------------------------------------------
# outside imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, render_template, make_response
import json
import os

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

# this is the index page. Going to http://localhost:5000/ when the
# project is running will bring you here
@app.route("/")
def index():
	events = [ e.json() for e in session.query( models.Event ).all() ]
	geo_url = get_geo_url()
	return render_template( 'index.html', geo_url=geo_url, events=events )

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
		path = os.path.join(LOCATION,'data/images/{}'.format(f.filename))
		f.save(path)

		image = models.Image( lat, lon, path )
		session.add(image)
		session.commit()

		return 'GOOD'

	except Exception as e:
		print(e)
		return 'BAD'


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

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
	messages = requests.values
	messages = messages.split(',')
	alert = utilities.alert_level(messages[0],messages[1])
	if alert == '0':
		response = 'You are in a low risk zone.'
	if alert == '1':
		response = 'You are in a moderate risk zone.'
	if alert == '2':
		response = 'You are in a high risk zone.'
	print(messages['msg'])
	resp = MessagingResponse()
	resp.message(response)
	return str(resp)

@app.route("/warning_level", methods=['GET'])
def warning_level():
	lat = request.values.get('lat')
	lon = request.values.get('lon')
	level = alert_level(lat,lon)
	return str(level)

if __name__ == "__main__":
	app.debug = True
	app.run()
