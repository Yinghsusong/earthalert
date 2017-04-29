# ------------------------------------------------------------------------------
# outside imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
		number = request.values.get('text')
		if number:
			person = models.Person()
			person.phone = number
		return render_template( 'report.html', number=number)
	else:
		return render_template( 'report.html')

if __name__ == "__main__":
	app.debug = True
	app.run()
