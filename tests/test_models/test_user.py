#!/usr/bin/python3
"""Test cases for User class"""
import unittest
import datetime
import json
import os
from models.user import User
from models.place import Place
from models.review import Review
from models import storage


class test_User(unittest.TestCase):
    """Test cases for User class"""

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
        instance = User()
        self.assertIsInstance(instance, User)

    def test_kwargs(self):
        """Test instantiation with kwargs"""
        data = {
            'id': '1234',
            'created_at': '2023-01-01T12:00:00',
            'updated_at': '2023-01-01T12:00:00',
            '__class__': 'User',
            'email': 'test@example.com',
            'password': 'password',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        instance = User(**data)
        self.assertEqual(instance.id, '1234')
        self.assertEqual(instance.created_at.isoformat(),
                         '2023-01-01T12:00:00')
        self.assertEqual(instance.updated_at.isoformat(),
                         '2023-01-01T12:00:00')
        self.assertEqual(instance.email, 'test@example.com')
        self.assertEqual(instance.password, 'password')
        self.assertEqual(instance.first_name, 'John')
        self.assertEqual(instance.last_name, 'Doe')

    def test_save(self):
        """Test save method"""
        instance = User()
        instance.save()
        key = "User." + instance.id
        with open('file.json', 'r') as f:
            data = json.load(f)
            self.assertIn(key, data)

    def test_str(self):
        """Test __str__ method"""
        instance = User()
        instance_str = str(instance)
        self.assertIn("[User]", instance_str)
        self.assertIn(instance.id, instance_str)
        self.assertIn("'created_at':", instance_str)
        self.assertIn("'updated_at':", instance_str)

    def test_to_dict(self):
        """Test to_dict method"""
        instance = User()
        instance_dict = instance.to_dict()
        self.assertEqual(instance_dict['__class__'], 'User')
        self.assertEqual(instance_dict['id'], instance.id)
        self.assertEqual(instance_dict['created_at'],
                         instance.created_at.isoformat())
        self.assertEqual(instance_dict['updated_at'],
                         instance.updated_at.isoformat())
        self.assertEqual(instance_dict['email'], instance.email)
        self.assertEqual(instance_dict['password'], instance.password)
        self.assertEqual(instance_dict['first_name'], instance.first_name)
        self.assertEqual(instance_dict['last_name'], instance.last_name)

    def test_places_relationship(self):
        """Test places relationship"""
        instance = User()
        place1 = Place(user_id=instance.id, name="Place 1")
        place2 = Place(user_id=instance.id, name="Place 2")
        instance.places.append(place1)
        instance.places.append(place2)
        storage.new(instance)
        storage.new(place1)
        storage.new(place2)
        storage.save()

        loaded_user = storage.all(User).values()
        self.assertEqual(len(loaded_user), 1)
        self.assertEqual(len(loaded_user[0].places), 2)
        self.assertIn(place1, loaded_user[0].places)
        self.assertIn(place2, loaded_user[0].places)

    def test_reviews_relationship(self):
        """Test reviews relationship"""
        instance = User()
        review1 = Review(user_id=instance.id, text="Review 1")
        review2 = Review(user_id=instance.id, text="Review 2")
        instance.reviews.append(review1)
        instance.reviews.append(review2)
        storage.new(instance)
        storage.new(review1)
        storage.new(review2)
        storage.save()

        loaded_user = storage.all(User).values()
        self.assertEqual(len(loaded_user), 1)
        self.assertEqual(len(loaded_user[0].reviews), 2)
        self.assertIn(review1, loaded_user[0].reviews)
        self.assertIn(review2, loaded_user[0].reviews)


if __name__ == '__main__':
    unittest.main()
