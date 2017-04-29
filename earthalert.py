# ------------------------------------------------------------------------------
# outside imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twilio.rest import Client
from flask import Flask, request, render_template, make_response

# local imports
from package import models

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
	return render_template( 'report.html' )




if __name__ == "__main__":
	app.debug = True
	app.run()
