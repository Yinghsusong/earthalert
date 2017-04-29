from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import csvx

Base = declarative_base()

class Event(Base):
	__tablename__ = 'event'
	id = Column(Integer, primary_key=True)
	date = Column(String(250))
	time = Column(String(250))
	country = Column(String(250))
	nearest_places = Column(String(250))
	hazard_type = Column(String(250))
	landslide_type = Column(String(250))
	trigger = Column(String(250))
	storm_name = Column(String(250))
	fatalities = Column(String(250))
	injuries = Column(String(250))
	source_name = Column(String(250))
	source_link = Column(String(250))
	location_description = Column(String(250))
	location_accuracy = Column(String(250))
	landslide_size = Column(String(250))
	photos_link = Column(String(250))
	cat_src = Column(String(250))
	cat_id = Column(String(250))
	countryname = Column(String(250))
	near = Column(String(250))
	distance = Column(String(250))
	adminname1 = Column(String(250))
	adminname2 = Column(String(250))
	population = Column(String(250))
	countrycode = Column(String(250))
	continentcode = Column(String(250))
	key = Column(String(250))
	version = Column(String(250))
	tstamp = Column(String(250))
	changeset_id = Column(String(250))
	latitude = Column(String(250))
	longitude = Column(String(250))
	geolocation = Column(String(250))

	def __init__( self, *args, **kwargs ):
		pass

	def set( self, **kwargs ):
		for key, value in kwargs.items():
			setattr(self,key,value)

def dump( dataset ):
	events = []
	with open( dataset, 'r', newline='' ) as _file:
		headings = _file.readline().split(',')
		csv = csvx.csv.Reader(_file)
		for row in csv:
			data = dict(zip(headings,row))
			event = Event()
			event.set( **data )
			events.append( event )
	return events

if __name__=='__main__':
	engine = create_engine('sqlite:///events.db')
	Session = sessionmaker(bind=engine)
	session = Session()

	Base.metadata.create_all(engine)

	events = dump( '/home/blankie/Work/python/earthalert/data/Global_Landslide_Catalog_Export.csv' )
	for event in events:
		session.add( event )
	session.commit()
