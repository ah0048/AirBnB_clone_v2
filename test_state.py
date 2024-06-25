#!/usr/bin/python3
"""Test module for State class"""

import unittest
from models.state import State
from models.city import City
from models import storage
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

class TestState(unittest.TestCase):
    """Test the State class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the test"""
        cls.engine = create_engine('mysql+mysqldb://root:root@localhost/hbnb_test_db')
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        """Tear down for the test"""
        cls.session.close()
        cls.engine.dispose()

    def test_relationship_with_city(self):
        """Test relationship between State and City"""
        state = State(name="California")
        self.session.add(state)
        self.session.commit()

        city = City(name="San Francisco", state_id=state.id)
        self.session.add(city)
        self.session.commit()

        self.assertEqual(city.state_id, state.id)

if __name__ == "__main__":
    unittest.main()
