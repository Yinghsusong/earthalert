from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

import json

from datetime import datetime

Base = declarative_base()

class Event(Base):
	__tablename__ = 'event'
	id = Column(Integer, primary_key=True)
	description = Column(String(250))
	datetime = Column(String(250))
	latitude = Column(String(250))
	longitude = Column(String(250))

	def __init__( self, lat, lon, desc ):
		self.datetime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
		self.latitude = str(lat)
		self.longitude = str(lon)
		self.description = str(desc)[:250]

	def json( self ):
		data = {
			"datetime":self.datetime,
			"latitude":self.latitude,
			"longitude":self.longitude,
			"description":self.description
		}
		return json.loads(json.dumps(data))


	def set( self, **kwargs ):
		for key, value in kwargs.items():
			setattr(self,key,value)

class Person(Base):
	__tablename__= 'people'
	id = Column(Integer, primary_key=True)
	phone = Column(String(250), unique=True)
	latitude = Column(String(250))
	longitude = Column(String(250))

	def set(self, latitude, longitude, phone):
		self.phone = phone
		self.latitude = latitude
		self.longitude = longitude

class Image(Base):
	__tablename__= 'images'
	id = Column(Integer, primary_key=True)
	path = Column(String(500), unique=True)
	latitude = Column(String(250))
	longitude = Column(String(250))

	def __init__(self, latitude, longitude, path):
		self.path = path
		self.latitude = latitude
		self.longitude = longitude

if __name__=='__main__':
	db_engine = create_engine( 'sqlite:///earthalert.db' )
	Base.metadata.create_all(db_engine)
