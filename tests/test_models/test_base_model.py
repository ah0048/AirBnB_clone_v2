#!/usr/bin/python3
"""Test cases for BaseModel class"""
import unittest
import datetime
import json
import os
from models.base_model import BaseModel
from models import storage


class test_basemodel(unittest.TestCase):
    """Test cases for BaseModel class"""

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
        instance = BaseModel()
        self.assertIsInstance(instance, BaseModel)

    def test_kwargs(self):
        """Test instantiation with kwargs"""
        data = {
            'id': '1234',
            'created_at': '2023-01-01T12:00:00',
            'updated_at': '2023-01-01T12:00:00',
            '__class__': 'BaseModel'
        }
        instance = BaseModel(**data)
        self.assertEqual(instance.id, '1234')
        self.assertEqual(instance.created_at.isoformat(),
                         '2023-01-01T12:00:00')
        self.assertEqual(instance.updated_at.isoformat(),
                         '2023-01-01T12:00:00')

    def test_save(self):
        """Test save method"""
        instance = BaseModel()
        initial_updated_at = instance.updated_at
        instance.save()
        self.assertNotEqual(instance.updated_at, initial_updated_at)

    def test_str(self):
        """Test __str__ method"""
        instance = BaseModel()
        instance_str = str(instance)
        self.assertIn("[BaseModel]", instance_str)
        self.assertIn(instance.id, instance_str)
        self.assertIn("'created_at':", instance_str)
        self.assertIn("'updated_at':", instance_str)

    def test_to_dict(self):
        """Test to_dict method"""
        instance = BaseModel()
        instance_dict = instance.to_dict()
        self.assertEqual(instance_dict['__class__'], 'BaseModel')
        self.assertEqual(instance_dict['id'], instance.id)
        self.assertEqual(instance_dict['created_at'],
                         instance.created_at.isoformat())
        self.assertEqual(instance_dict['updated_at'],
                         instance.updated_at.isoformat())

    def test_delete(self):
        """Test delete method"""
        instance = BaseModel()
        storage.new(instance)
        storage.save()
        initial_count = len(storage.all())
        instance.delete()
        storage.save()
        self.assertEqual(len(storage.all()), initial_count - 1)

    def test_delete_none(self):
        """Test delete method with None argument"""
        instance = BaseModel()
        storage.new(instance)
        storage.save()
        initial_count = len(storage.all())
        storage.delete(None)
        storage.save()
        self.assertEqual(len(storage.all()), initial_count)

    def test_instance_not_in_storage_after_delete(self):
        """Test instance is removed from storage after delete"""
        instance = BaseModel()
        storage.new(instance)
        storage.save()
        key = "{}.{}".format(instance.__class__.__name__, instance.id)
        self.assertIn(key, storage.all())
        instance.delete()
        storage.save()
        self.assertNotIn(key, storage.all())

    def test_kwargs_invalid(self):
        """Test instantiation with invalid kwargs"""
        invalid_data = {
            'invalid_key': 'value'
        }
        with self.assertRaises(TypeError):
            BaseModel(**invalid_data)

    def test_id_type(self):
        """Test type of id attribute"""
        instance = BaseModel()
        self.assertIsInstance(instance.id, str)

    def test_created_at_type(self):
        """Test type of created_at attribute"""
        instance = BaseModel()
        self.assertIsInstance(instance.created_at, datetime.datetime)

    def test_updated_at_type(self):
        """Test type of updated_at attribute"""
        instance = BaseModel()
        self.assertIsInstance(instance.updated_at, datetime.datetime)
        self.assertEqual(instance.created_at, instance.updated_at)

    def test_updated_at_after_save(self):
        """Test updated_at changes after save"""
        instance = BaseModel()
        initial_updated_at = instance.updated_at
        instance.save()
        self.assertNotEqual(instance.updated_at, initial_updated_at)


if __name__ == '__main__':
    unittest.main()
