#!/usr/bin/python3
""" handle database storage"""
from sqlalchemy import create_engine
from os import getenv
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.review import Review
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """
        crate engine
        """
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user,
            password,
            host,
            db
        ), pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the database on all objects"""
        models = [User, State, City, Amenity, Place, Review]
        objs_dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            q = self.__session.query(cls)
            for obj in q:
                k = "{}.{}".format(obj.__class__.__name__, obj.id)
                objs_dict[k] = obj
            return objs_dict
        else:
            for model in models:
                q = self.__session.query(model)
                for obj in q:
                    k = "{}.{}".format(obj.__class__.__name__, obj.id)
                    objs_dict[k] = obj
            return objs_dict
    def new(self, obj):
        """ to add new object to the current db"""
        self.__session.add(obj)

    def save(self):
        """commit all changes which occured durring session"""
        self.__session.commit()
    def delete(self, obj=None):
        """ to delet object from db"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in databas"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))

    def close(self):
        """to close the current session"""
        self.__session.close()
