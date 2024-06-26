#!/usr/bin/python3
"""Module for testing DBStorage"""
import unittest
from models import storage
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

class TestDBStorage(unittest.TestCase):
    """Class to test the DBStorage method"""

    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        # Set up the environment variables for the test database
        os.environ['HBNB_MYSQL_USER'] = 'hbnb_test'
        os.environ['HBNB_MYSQL_PWD'] = 'hbnb_test_pwd'
        os.environ['HBNB_MYSQL_HOST'] = 'localhost'
        os.environ['HBNB_MYSQL_DB'] = 'hbnb_test_db'
        os.environ['HBNB_ENV'] = 'test'
        os.environ['HBNB_TYPE_STORAGE'] = 'db'  # Set the storage type to 'db'

        # Create the engine and session for the test database
        from models.engine.db_storage import DBStorage
        cls.storage = DBStorage()
        cls.storage.reload()
        cls.session = cls.storage._DBStorage__session

    @classmethod
    def tearDownClass(cls):
        """Remove test database at the end of the tests"""
        # Drop all tables
        Base.metadata.drop_all(cls.storage._DBStorage__engine)

        # Close the session
        cls.session.remove()

    def setUp(self):
        """Start a session for each test"""
        self.session = self.storage._DBStorage__session

    def tearDown(self):
        """Rollback the session after each test"""
        self.session.rollback()

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new(self):
        """Test that new adds an object to the database"""
        state = State(name="California")
        self.storage.new(state)
        self.storage.save()
        self.assertIn(state, self.session)

    def test_save(self):
        """Test that save commits the changes to the database"""
        state = State(name="California")
        self.storage.new(state)
        self.storage.save()
        self.assertIn(state, self.session)

    def test_delete(self):
        """Test that delete removes an object from the database"""
        state = State(name="California")
        self.storage.new(state)
        self.storage.save()
        self.storage.delete(state)
        self.storage.save()
        self.assertNotIn(state, self.session)

    def test_reload(self):
        """Test that reload creates all tables"""
        self.storage.reload()
        self.assertTrue(self.session)

    def test_all_with_class(self):
        """Test that all returns all objects of a given class"""
        state = State(name="California")
        self.storage.new(state)
        self.storage.save()
        objects = self.storage.all(State)
        self.assertIn(state, objects.values())

    def test_all_without_class(self):
        """Test that all returns all objects when no class is passed"""
        state = State(name="California")
        city = City(name="San Francisco", state_id=state.id)
        self.storage.new(state)
        self.storage.new(city)
        self.storage.save()
        objects = self.storage.all()
        self.assertIn(state, objects.values())
        self.assertIn(city, objects.values())

    def test_new_method(self):
        """Test new method"""
        new_state = State(name="California")
        self.storage.new(new_state)
        self.storage.save()
        self.assertIn(new_state, self.session.query(State).all())

    def test_delete_method(self):
        """Test delete method"""
        new_state = State(name="California")
        self.storage.new(new_state)
        self.storage.save()
        self.storage.delete(new_state)
        self.storage.save()
        self.assertNotIn(new_state, self.session.query(State).all())

    def test_reload_method(self):
        """Test reload method"""
        self.storage.reload()
        self.assertIsNotNone(self.storage._DBStorage__session)


if __name__ == '__main__':
    unittest.main()
