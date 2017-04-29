from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Event(Base):
	__tablename__ = 'event'
	id = Column(Integer, primary_key=True)
	date = Column(String(250))
	time = Column(String(250))
	location = Column(String(250))
	latitude = Column(String(250))
	longitude = Column(String(250))

	def __init__( self, *args, **kwargs ):
		pass

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

if __name__=='__main__':
	db_engine = create_engine( 'sqlite:///earthalert.db' )
	Base.metadata.create_all(db_engine)
