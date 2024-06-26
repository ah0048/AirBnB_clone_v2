#!/usr/bin/python3
"""Test cases for City class"""
import unittest
import datetime
import json
import os
from models.city import City
from models.state import State
from models.place import Place
from models import storage


class test_City(unittest.TestCase):
    """Test cases for City class"""

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
        instance = City()
        self.assertIsInstance(instance, City)

    def test_kwargs(self):
        """Test instantiation with kwargs"""
        data = {
            'id': '1234',
            'created_at': '2023-01-01T12:00:00',
            'updated_at': '2023-01-01T12:00:00',
            '__class__': 'City',
            'name': 'San Francisco',
            'state_id': '5678'
        }
        instance = City(**data)
        self.assertEqual(instance.id, '1234')
        self.assertEqual(instance.created_at.isoformat(),
                         '2023-01-01T12:00:00')
        self.assertEqual(instance.updated_at.isoformat(),
                         '2023-01-01T12:00:00')
        self.assertEqual(instance.name, 'San Francisco')
        self.assertEqual(instance.state_id, '5678')

    def test_save(self):
        """Test save method"""
        instance = City()
        instance.save()
        key = "City." + instance.id
        with open('file.json', 'r') as f:
            data = json.load(f)
            self.assertIn(key, data)

    def test_str(self):
        """Test __str__ method"""
        instance = City()
        instance_str = str(instance)
        self.assertIn("[City]", instance_str)
        self.assertIn(instance.id, instance_str)
        self.assertIn("'created_at':", instance_str)
        self.assertIn("'updated_at':", instance_str)

    def test_to_dict(self):
        """Test to_dict method"""
        instance = City()
        instance_dict = instance.to_dict()
        self.assertEqual(instance_dict['__class__'], 'City')
        self.assertEqual(instance_dict['id'], instance.id)
        self.assertEqual(instance_dict['created_at'],
                         instance.created_at.isoformat())
        self.assertEqual(instance_dict['updated_at'],
                         instance.updated_at.isoformat())
        self.assertEqual(instance_dict['name'], instance.name)
        self.assertEqual(instance_dict['state_id'], instance.state_id)

    def test_places_relationship(self):
        """Test places relationship"""
        state = State(name="California")
        city = City(name="San Francisco", state_id=state.id)
        place1 = Place(city_id=city.id, name="Place 1")
        place2 = Place(city_id=city.id, name="Place 2")
        city.places.append(place1)
        city.places.append(place2)
        storage.new(state)
        storage.new(city)
        storage.new(place1)
        storage.new(place2)
        storage.save()

        loaded_city = storage.all(City).values()
        self.assertEqual(len(loaded_city), 1)
        self.assertEqual(len(loaded_city[0].places), 2)
        self.assertIn(place1, loaded_city[0].places)
        self.assertIn(place2, loaded_city[0].places)


if __name__ == '__main__':
    unittest.main()
