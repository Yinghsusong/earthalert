# ------------------------------------------------------------------------------
# outside imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, render_template, make_response
import json

# local imports
from package import models
from package.utilities import *

# initial setup
db_engine = create_engine( 'sqlite:///earthalert.db' )
session_generator = sessionmaker(bind=db_engine)
session = session_generator()

# init the app
app = Flask(__name__)

# this is the index page. Going to http://localhost:5000/ when the
# project is running will bring you here
@app.route("/")
def index():
	events = session.query( models.Event ).all()
	geo_url = get_geo_url()
	return render_template( 'index.html', geo_url=geo_url )

@app.route("/report", methods=['POST'])
def report():
	lat = request.values.get('lat')
	lon = request.values.get('lon')
	event = Event( lat, lon )
	session.add(  )

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
	print(messages['msg'])
	resp = MessagingResponse()

	resp.message("test msg")
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
