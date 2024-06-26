#!/usr/bin/python3
"""Test cases for Review class"""
import unittest
from models.review import Review
from models.place import Place
from models.user import User
import os
import json
from datetime import datetime
from models import storage


class test_Review(unittest.TestCase):
    """Test cases for Review class"""

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
        instance = Review()
        self.assertIsInstance(instance, Review)

    def test_kwargs(self):
        """Test instantiation with kwargs"""
        data = {
            'id': '1234',
            'created_at': '2023-01-01T12:00:00',
            'updated_at': '2023-01-01T12:00:00',
            '__class__': 'Review',
            'place_id': '5678',
            'user_id': '9012',
            'text': 'Test review'
        }
        instance = Review(**data)
        self.assertEqual(instance.id, '1234')
        self.assertEqual(instance.created_at.isoformat(),
                         '2023-01-01T12:00:00')
        self.assertEqual(instance.updated_at.isoformat(),
                         '2023-01-01T12:00:00')
        self.assertEqual(instance.place_id, '5678')
        self.assertEqual(instance.user_id, '9012')
        self.assertEqual(instance.text, 'Test review')

    def test_save(self):
        """Test save method"""
        instance = Review()
        instance.save()
        key = "Review." + instance.id
        with open('file.json', 'r') as f:
            data = json.load(f)
            self.assertIn(key, data)

    def test_str(self):
        """Test __str__ method"""
        instance = Review()
        instance_str = str(instance)
        self.assertIn("[Review]", instance_str)
        self.assertIn(instance.id, instance_str)
        self.assertIn("'created_at':", instance_str)
        self.assertIn("'updated_at':", instance_str)

    def test_to_dict(self):
        """Test to_dict method"""
        instance = Review()
        instance_dict = instance.to_dict()
        self.assertEqual(instance_dict['__class__'], 'Review')
        self.assertEqual(instance_dict['id'], instance.id)
        self.assertEqual(instance_dict['created_at'],
                         instance.created_at.isoformat())
        self.assertEqual(instance_dict['updated_at'],
                         instance.updated_at.isoformat())
        self.assertEqual(instance_dict['place_id'], instance.place_id)
        self.assertEqual(instance_dict['user_id'], instance.user_id)
        self.assertEqual(instance_dict['text'], instance.text)

    def test_place_relationship(self):
        """Test place relationship"""
        place = Place()
        instance = Review(place_id=place.id)
        storage.new(place)
        storage.new(instance)
        storage.save()

        loaded_review = storage.all(Review).values()
        self.assertEqual(len(loaded_review), 1)
        self.assertEqual(loaded_review[0].place_id, place.id)

    def test_user_relationship(self):
        """Test user relationship"""
        user = User()
        instance = Review(user_id=user.id)
        storage.new(user)
        storage.new(instance)
        storage.save()

        loaded_review = storage.all(Review).values()
        self.assertEqual(len(loaded_review), 1)
        self.assertEqual(loaded_review[0].user_id, user.id)


if __name__ == '__main__':
    unittest.main()
