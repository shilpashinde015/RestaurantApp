import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    user_id = Column(String(250), nullable=False)
    provider = Column(String(250), nullable=False)

    # Code to define what to send (in each restaurant) in JSON format
    @property
    def serialize(self):
        # Returns data in easily serializable format (like dictionary format)
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
            'picture': self.picture,
            'user_id': self.user_id,
            'provider': self.provider
        }

class Restaurant(Base):
        __tablename__ = 'restaurant'
        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable = False)

        @property
        def serialize(self):
            """Return object data in easily serializeable format"""
            return {
            'name': self.name,
            'id': self.id,
            }


class MenuItem(Base):
    __tablename__='menu_item'

    name = Column(String(80),nullable = False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    restaurant =  relationship(Restaurant)

    # serializable format
    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
db_secrets_path = os.path.join(PROJECT_ROOT, 'database_secrets.json')
#
# user = json.loads(
#         open(db_secrets_path, 'r').read()
#     )["postgresql"]["user"]
# password = json.loads(
#         open(db_secrets_path, 'r').read()
#     )["postgresql"]["password"]
# database = json.loads(
#         open(db_secrets_path, 'r').read()
#     )["postgresql"]["database"]

# Instance of create engine class and point to database we use
# engine = create_engine(
#     'postgresql://{user}:{password}@localhost:5432/{database}'.format(
#         user=user,
#         password=password,
#         database=database
#     )
# )


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
