#!/usr/bin/python3
""" module for state name """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from os import getenv
from sqlalchemy import Column, String


class State(BaseModel, Base):
    """state : the name of state"""

    __tablename__ = "states"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade='all, delete', backref='state')
    else:
        """ file storage relationship"""
        @property
        def cities(self):
            """return all cities related in state"""
            from models import storage
            from models.city import City

            Cities = []
            city_dict = storage.all(City)
            for city in city_dict.values():
                if city.state_id == self.id:
                    Cities.append(city)
            return Cities
