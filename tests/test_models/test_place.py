#!/usr/bin/python3
"""Test cases for Place class"""
import unittest
import json
import os
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models import storage


class test_Place(unittest.TestCase):
    """Test cases for Place class"""

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
        instance = Place()
        self.assertIsInstance(instance, Place)

    def test_kwargs(self):
        """Test instantiation with kwargs"""
        data = {
            'id': '1234',
            'created_at': '2023-01-01T12:00:00',
            'updated_at': '2023-01-01T12:00:00',
            '__class__': 'Place',
            'city_id': '5678',
            'user_id': '9012',
            'name': 'Test Place',
            'description': 'Test description',
            'number_rooms': 2,
            'number_bathrooms': 1,
            'max_guest': 4,
            'price_by_night': 100,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'amenity_ids': ['3456', '7890']
        }
        instance = Place(**data)
        self.assertEqual(instance.id, '1234')
        self.assertEqual(instance.created_at.isoformat(),
                         '2023-01-01T12:00:00')
        self.assertEqual(instance.updated_at.isoformat(),
                         '2023-01-01T12:00:00')
        self.assertEqual(instance.city_id, '5678')
        self.assertEqual(instance.user_id, '9012')
        self.assertEqual(instance.name, 'Test Place')
        self.assertEqual(instance.description, 'Test description')
        self.assertEqual(instance.number_rooms, 2)
        self.assertEqual(instance.number_bathrooms, 1)
        self.assertEqual(instance.max_guest, 4)
        self.assertEqual(instance.price_by_night, 100)
        self.assertEqual(instance.latitude, 37.7749)
        self.assertEqual(instance.longitude, -122.4194)
        self.assertEqual(instance.amenity_ids, ['3456', '7890'])

    def test_save(self):
        """Test save method"""
        instance = Place()
        instance.save()
        key = "Place." + instance.id
        with open('file.json', 'r') as f:
            data = json.load(f)
            self.assertIn(key, data)

    def test_str(self):
        """Test __str__ method"""
        instance = Place()
        instance_str = str(instance)
        self.assertIn("[Place]", instance_str)
        self.assertIn(instance.id, instance_str)
        self.assertIn("'created_at':", instance_str)
        self.assertIn("'updated_at':", instance_str)

    def test_to_dict(self):
        """Test to_dict method"""
        instance = Place()
        instance_dict = instance.to_dict()
        self.assertEqual(instance_dict['__class__'], 'Place')
        self.assertEqual(instance_dict['id'], instance.id)
        self.assertEqual(instance_dict['created_at'],
                         instance.created_at.isoformat())
        self.assertEqual(instance_dict['updated_at'],
                         instance.updated_at.isoformat())
        self.assertEqual(instance_dict['city_id'], instance.city_id)
        self.assertEqual(instance_dict['user_id'], instance.user_id)
        self.assertEqual(instance_dict['name'], instance.name)
        self.assertEqual(instance_dict['description'], instance.description)
        self.assertEqual(instance_dict['number_rooms'], instance.number_rooms)
        self.assertEqual(instance_dict['number_bathrooms'],
                         instance.number_bathrooms)
        self.assertEqual(instance_dict['max_guest'], instance.max_guest)
        self.assertEqual(instance_dict['price_by_night'],
                         instance.price_by_night)
        self.assertEqual(instance_dict['latitude'], instance.latitude)
        self.assertEqual(instance_dict['longitude'], instance.longitude)
        self.assertEqual(instance_dict['amenity_ids'], instance.amenity_ids)

    def test_city_relationship(self):
        """Test city relationship"""
        city = City()
        instance = Place(city_id=city.id)
        storage.new(city)
        storage.new(instance)
        storage.save()

        loaded_place = storage.all(Place).values()
        self.assertEqual(len(loaded_place), 1)
        self.assertEqual(loaded_place[0].city_id, city.id)

    def test_user_relationship(self):
        """Test user relationship"""
        user = User()
        instance = Place(user_id=user.id)
        storage.new(user)
        storage.new(instance)
        storage.save()

        loaded_place = storage.all(Place).values()
        self.assertEqual(len(loaded_place), 1)
        self.assertEqual(loaded_place[0].user_id, user.id)

    def test_reviews_relationship(self):
        """Test reviews relationship"""
        instance = Place()
        review1 = Review(place_id=instance.id, text="Review 1")
        review2 = Review(place_id=instance.id, text="Review 2")
        instance.reviews.append(review1)
        instance.reviews.append(review2)
        storage.new(instance)
        storage.new(review1)
        storage.new(review2)
        storage.save()

        loaded_place = storage.all(Place).values()
        self.assertEqual(len(loaded_place), 1)
        self.assertEqual(len(loaded_place[0].reviews), 2)
        self.assertIn(review1, loaded_place[0].reviews)
        self.assertIn(review2, loaded_place[0].reviews)

    def test_amenities_relationship(self):
        """Test amenities relationship"""
        instance = Place()
        amenity1 = Amenity(name="Amenity 1")
        amenity2 = Amenity(name="Amenity 2")
        instance.amenities.append(amenity1)
        instance.amenities.append(amenity2)
        storage.new(instance)
        storage.new(amenity1)
        storage.new(amenity2)
        storage.save()

        loaded_place = storage.all(Place).values()
        self.assertEqual(len(loaded_place), 1)
        self.assertEqual(len(loaded_place[0].amenities), 2)
        self.assertIn(amenity1, loaded_place[0].amenities)
        self.assertIn(amenity2, loaded_place[0].amenities)


if __name__ == '__main__':
    unittest.main()
