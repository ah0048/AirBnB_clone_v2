#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models.place import Place
from models.state import State
from models import storage
import os
from console import HBNBCommand
from io import StringIO
from contextlib import redirect_stdout


class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]
        self.console = HBNBCommand()

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except Exception as e:
            raise RuntimeError(f"Failed to remove 'file.json': {e}")

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_all_with_class(self):
        """ __objects is properly returned filtered by class """
        new_state = State(name="California")
        new_place = Place(name="My_little_house")
        storage.new(new_state)
        storage.new(new_place)
        storage.save()
        states = storage.all(State)
        places = storage.all(Place)
        self.assertIn(new_state, states.values())
        self.assertNotIn(new_place, states.values())
        self.assertIn(new_place, places.values())
        self.assertNotIn(new_state, places.values())

    def test_delete(self):
        """ Delete object from __objects if it's inside """
        new = BaseModel()
        storage.new(new)
        storage.save()
        self.assertIn(new, storage.all().values())
        storage.delete(new)
        storage.save()
        self.assertNotIn(new, storage.all().values())

    def test_delete_none(self):
        """ Test delete with obj=None does nothing """
        initial_count = len(storage.all())
        storage.delete(None)
        self.assertEqual(len(storage.all()), initial_count)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        storage.save()
        storage.reload()
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        print(type(storage))
        self.assertEqual(type(storage), FileStorage)

    def test_create_with_parameters(self):
        """ Test create command with parameters """
        # Capture the output of the command
        with StringIO() as buf, redirect_stdout(buf):
            self.console.onecmd('create Place name="My_little_house"\
                                 number_rooms=4 number_bathrooms=2\
                                 max_guest=10\
                                 price_by_night=300\
                                 latitude=37.773972 longitude=-122.431297')
            output = buf.getvalue().strip()

        # Ensure an ID is printed (ID of the created Place)
        self.assertTrue(len(output) > 0)

        # Verify the Place was created with the correct attributes
        place = storage.all()["Place." + output]
        self.assertEqual(place.name, "My little house")
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.max_guest, 10)
        self.assertEqual(place.price_by_night, 300)
        self.assertAlmostEqual(place.latitude, 37.773972)
        self.assertAlmostEqual(place.longitude, -122.431297)

    def test_create_with_invalid_parameters(self):
        """ Test create command with invalid parameters """
        # Capture the output of the command
        with StringIO() as buf, redirect_stdout(buf):
            self.console.onecmd('create Place name="My_little_house"\
                                 invalid_param=some_value')
            output = buf.getvalue().strip()

        # Ensure an ID is printed (ID of the created Place)
        self.assertTrue(len(output) > 0)

        # Verify the Place was created and invalid_param was ignored
        place = storage.all()["Place." + output]
        self.assertEqual(place.name, "My little house")
        self.assertFalse(hasattr(place, 'invalid_param'))


if __name__ == '__main__':
    unittest.main()
