#!/usr/bin/python3
"""Test cases for State class"""
import unittest
import datetime
import json
import os
from models.state import State
from models.city import City
from models import storage


class test_state(unittest.TestCase):
    """Test cases for State class"""

    def setUp(self):
        """Set up test environment"""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def tearDown(self):
        """Clean up after each test"""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass

    def test_default(self):
        """Test default instantiation"""
        instance = State()
        self.assertIsInstance(instance, State)

    def test_kwargs(self):
        """Test instantiation with kwargs"""
        data = {
            'id': '1234',
            'created_at': '2023-01-01T12:00:00',
            'updated_at': '2023-01-01T12:00:00',
            '__class__': 'State',
            'name': 'California'
        }
        instance = State(**data)
        self.assertEqual(instance.id, '1234')
        self.assertEqual(instance.created_at.isoformat(),
                         '2023-01-01T12:00:00')
        self.assertEqual(instance.updated_at.isoformat(),
                         '2023-01-01T12:00:00')
        self.assertEqual(instance.name, 'California')

    def test_save(self):
        """Test save method"""
        instance = State()
        instance.save()
        key = "State." + instance.id
        with open('file.json', 'r') as f:
            data = json.load(f)
            self.assertIn(key, data)

    def test_str(self):
        """Test __str__ method"""
        instance = State()
        instance_str = str(instance)
        self.assertIn("[State]", instance_str)
        self.assertIn(instance.id, instance_str)
        self.assertIn("'created_at':", instance_str)
        self.assertIn("'updated_at':", instance_str)

    def test_to_dict(self):
        """Test to_dict method"""
        instance = State()
        instance_dict = instance.to_dict()
        self.assertEqual(instance_dict['__class__'], 'State')
        self.assertEqual(instance_dict['id'], instance.id)
        self.assertEqual(instance_dict['created_at'],
                         instance.created_at.isoformat())
        self.assertEqual(instance_dict['updated_at'],
                         instance.updated_at.isoformat())
        self.assertEqual(instance_dict['name'], instance.name)

    def test_cities_property(self):
        """Test cities property"""
        state = State(name="California")
        city1 = City(state_id=state.id, name="Los Angeles")
        city2 = City(state_id=state.id, name="San Francisco")
        storage.new(state)
        storage.new(city1)
        storage.new(city2)
        storage.save()

        cities = state.cities
        self.assertEqual(len(cities), 2)
        self.assertIn(city1, cities)
        self.assertIn(city2, cities)

    def test_cities_relationship(self):
        """Test cities relationship"""
        state = State(name="California")
        city1 = City(state_id=state.id, name="Los Angeles")
        city2 = City(state_id=state.id, name="San Francisco")
        state.cities.append(city1)
        state.cities.append(city2)
        storage.new(state)
        storage.save()

        loaded_state = storage.all(State).values()
        self.assertEqual(len(loaded_state), 1)
        self.assertEqual(len(loaded_state[0].cities), 2)
        self.assertIn(city1, loaded_state[0].cities)
        self.assertIn(city2, loaded_state[0].cities)


if __name__ == '__main__':
    unittest.main()
