import unittest
from unittest.mock import patch
from models.base_model import BaseModel
from datetime import datetime
import json


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        # Create an instance of BaseModel for testing
        self.base_model = BaseModel()

    def test_init(self):
        # Assert that the ID is a string
        self.assertIsInstance(self.base_model.id, str)
        # Assert that created_at and updated_at are datetime objects
        self.assertIsInstance(self.base_model.created_at, datetime)
        self.assertIsInstance(self.base_model.updated_at, datetime)

    def test_save(self):
        # Save the initial updated_at value
        initial_updated_at = self.base_model.updated_at
        # Call the save method
        self.base_model.save()
        # Assert that updated_at has changed after calling save
        self.assertNotEqual(initial_updated_at, self.base_model.updated_at)

    def test_to_dict(self):
        # Convert the BaseModel instance to a dictionary
        base_model_dict = self.base_model.to_dict()
        # Assert that keys exist in the dictionary
        self.assertIn("id", base_model_dict)
        self.assertIn("created_at", base_model_dict)
        self.assertIn("updated_at", base_model_dict)
        self.assertIn("__class__", base_model_dict)
        # Assert that values are of the expected types
        self.assertIsInstance(base_model_dict["id"], str)
        self.assertIsInstance(base_model_dict["created_at"], str)
        self.assertIsInstance(base_model_dict["updated_at"], str)
        self.assertIsInstance(base_model_dict["__class__"], str)

    def test_str(self):
        # Convert the BaseModel instance to a string
        base_model_str = str(self.base_model)
        # Assert that the string representation contains class name and id
        self.assertIn(self.base_model.__class__.__name__, base_model_str)
        self.assertIn(self.base_model.id, base_model_str)
        # Add more specific assertions based on your BaseModel implementation

    def test_init_with_kwargs(self):
        # Test initializing with specific values using kwargs
        data = {
            "id": "test_id",
            "created_at": "2022-01-01T00:00:00.000000",
            "updated_at": "2022-01-02T00:00:00.000000",
            "custom_attribute": "custom_value"
        }
        base_model = BaseModel(**data)
        self.assertEqual(base_model.id, data["id"])
        self.assertEqual(base_model.created_at, datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(base_model.updated_at, datetime.strptime(data["updated_at"], "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(base_model.custom_attribute, "custom_value")

    def test_save_multiple_instances(self):
        # Test saving multiple instances and check if their updated_at values change
        base_model1 = BaseModel()
        base_model2 = BaseModel()
        initial_updated_at1 = base_model1.updated_at
        initial_updated_at2 = base_model2.updated_at

        base_model1.save()
        base_model2.save()

        self.assertNotEqual(initial_updated_at1, base_model1.updated_at)
        self.assertNotEqual(initial_updated_at2, base_model2.updated_at)

    def test_to_dict_values(self):
        # Test if the values in the to_dict() output match the actual attribute values
        base_model_dict = self.base_model.to_dict()
        self.assertEqual(base_model_dict["id"], self.base_model.id)
        self.assertEqual(base_model_dict["created_at"], self.base_model.created_at)
        self.assertEqual(base_model_dict["updated_at"], self.base_model.updated_at)
        self.assertEqual(base_model_dict["__class__"], self.base_model.__class__.__name__)

if __name__ == '__main__':
    unittest.main()
