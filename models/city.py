#!/usr/bin/python3
""" module for the city """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import ForeignKey, String, Column


class City(BaseModel, Base):
    """ represnt tha name of the city and state id """

    __tablename__ = "cities"

    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
