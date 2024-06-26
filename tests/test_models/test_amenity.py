#!/usr/bin/python3
"""Test cases for Amenity class"""
import unittest
from models.amenity import Amenity
from models.place import Place
import os
import json
from models import storage


class test_Amenity(unittest.TestCase):
    """Test cases for Amenity class"""

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
        instance = Amenity()
        self.assertIsInstance(instance, Amenity)

    def test_kwargs(self):
        """Test instantiation with kwargs"""
        data = {
            'id': '1234',
            'created_at': '2023-01-01T12:00:00',
            'updated_at': '2023-01-01T12:00:00',
            '__class__': 'Amenity',
            'name': 'Test amenity'
        }
        instance = Amenity(**data)
        self.assertEqual(instance.id, '1234')
        self.assertEqual(instance.created_at.isoformat(),
                         '2023-01-01T12:00:00')
        self.assertEqual(instance.updated_at.isoformat(),
                         '2023-01-01T12:00:00')
        self.assertEqual(instance.name, 'Test amenity')

    def test_save(self):
        """Test save method"""
        instance = Amenity()
        instance.save()
        key = "Amenity." + instance.id
        with open('file.json', 'r') as f:
            data = json.load(f)
            self.assertIn(key, data)

    def test_str(self):
        """Test __str__ method"""
        instance = Amenity()
        instance_str = str(instance)
        self.assertIn("[Amenity]", instance_str)
        self.assertIn(instance.id, instance_str)
        self.assertIn("'created_at':", instance_str)
        self.assertIn("'updated_at':", instance_str)

    def test_to_dict(self):
        """Test to_dict method"""
        instance = Amenity()
        instance_dict = instance.to_dict()
        self.assertEqual(instance_dict['__class__'], 'Amenity')
        self.assertEqual(instance_dict['id'], instance.id)
        self.assertEqual(instance_dict['created_at'],
                         instance.created_at.isoformat())
        self.assertEqual(instance_dict['updated_at'],
                         instance.updated_at.isoformat())
        self.assertEqual(instance_dict['name'], instance.name)

    def test_place_relationship(self):
        """Test place relationship"""
        place = Place()
        instance = Amenity(name='WiFi')
        instance.places.append(place)
        storage.new(place)
        storage.new(instance)
        storage.save()

        loaded_amenity = storage.all(Amenity).values()
        self.assertEqual(len(loaded_amenity), 1)
        self.assertEqual(len(loaded_amenity[0].places), 1)
        self.assertEqual(loaded_amenity[0].places[0], place.id)


if __name__ == '__main__':
    unittest.main()
