#!/usr/bin/python3
'''New engine to be linked with my database'''
from models.base_model import Base, BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os


class DBStorage:
    '''database storage'''
    __engine = None
    __session = None

    def __init__(self):
        '''constructor to start engine'''

        mysql_user = os.getenv('HBNB_MYSQL_USER')
        mysql_passwd = os.getenv('HBNB_MYSQL_PWD')
        mysql_host = os.getenv('HBNB_MYSQL_HOST')
        mysql_db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        conn_string = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
            mysql_user, mysql_passwd, mysql_host, mysql_db)
        self.__engine = create_engine(conn_string, pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''query on the current database session for a class'''

        objects = {}
        classes = [State, City]
        if cls is not None:
            query = self.__session.query(cls).all()
            for obj in query:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objects[key] = obj
        else:
            for each_class in classes:
                query = self.__session.query(each_class).all()
                for obj in query:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        '''add the object to the current database session'''

        self.__session.add(obj)

    def save(self):
        '''commit all changes of the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''delete from the current database session'''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''create all tables and current session'''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)




