from package import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
db_engine = create_engine( 'earthalert.db' )
session_generator = sessionmaker(bind=db_engine)
session = session_generator()

from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
	events = session.query( models.Event ).all()
	return render_template( 'index.html', events=events )

if __name__ == "__main__":
    app.run()
