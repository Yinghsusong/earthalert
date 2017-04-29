# ------------------------------------------------------------------------------
# outside imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twilio.rest import Client
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
	return render_template( 'index.html', events=events )

# this is the index page. Going to http://localhost:5000/ when the
# project is running will bring you here

@app.route("/report", methods=[ 'GET', 'POST'])
def report():
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
				account_sid = 'ACb9b3ae8e3b69b1fba8a0f14b9faf2042'
				auth_token = '885b48598f6934e4f98df504efe239a4'
				"""client = Client(account_sid,auth_token)
				message = client.messages.create(
					to = '+12566985523',
					from_ = '+12563611028',
					body = 'This is a test message for the website')
				print(message.sid)"""
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

@app.route("/warning_level", methods=['POST'])
def warning_level():
	lat = request.values.get('lat')
	lon = request.values.get('lon')
	danger_level = alert_level(lat, lon)
	return danger_level
	print(danger_level)

if __name__ == "__main__":
	app.debug = True
	app.run()
