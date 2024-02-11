import unittest
from unittest.mock import patch
from models.base_model import BaseModel
from datetime import datetime, timedelta
import json
import os


class TestBaseModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.backup_file = "backup_file.json"
        if os.path.exists("file.json"):
            os.rename("file.json", cls.backup_file)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.backup_file):
            os.rename(cls.backup_file, "file.json")

    def setUp(self):
        with open("file.json", "w") as f:
            f.write("")

    def tearDown(self):
        with open("file.json", "w") as f:
            f.write("")

    def test_init(self):
        bm = BaseModel()
        self.assertIsInstance(bm.id, str)
        self.assertIsInstance(bm.created_at, datetime)
        self.assertIsInstance(bm.updated_at, datetime)

    def test_save(self):
        bm = BaseModel()
        initial_updated_at = bm.updated_at
        bm.save()
        self.assertNotEqual(initial_updated_at, bm.updated_at)

    def test_to_dict(self):
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertIn("id", bm_dict)
        self.assertIn("created_at", bm_dict)
        self.assertIn("updated_at", bm_dict)
        self.assertIn("__class__", bm_dict)

    def test_str(self):
        bm = BaseModel()
        bm_str = str(bm)
        self.assertIn("[BaseModel]", bm_str)
        self.assertIn(bm.id, bm_str)

    def test_init_with_kwargs(self):
        data = {
            "id": "test_id",
            "created_at": "2022-01-01T00:00:00.000000",
            "updated_at": "2022-01-02T00:00:00.000000",
            "custom_attribute": "custom_value"
        }
        i = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel(**data)
        self.assertEqual(bm.id, data["id"])
        self.assertEqual(bm.created_at,
                         datetime.strptime(data["created_at"], i))
        self.assertEqual(bm.updated_at,
                         datetime.strptime(data["updated_at"], i))
        self.assertEqual(bm.custom_attribute, "custom_value")

    def test_save_multiple_instances(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        initial_updated_at1 = bm1.updated_at
        initial_updated_at2 = bm2.updated_at

        bm1.save()
        bm2.save()

        self.assertNotEqual(initial_updated_at1, bm1.updated_at)
        self.assertNotEqual(initial_updated_at2, bm2.updated_at)

    def test_to_dict_values(self):
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(bm_dict["id"], bm.id)
        self.assertEqual(bm_dict["created_at"], bm.created_at.isoformat())
        self.assertEqual(bm_dict["updated_at"], bm.updated_at.isoformat())
        self.assertEqual(bm_dict["__class__"], bm.__class__.__name__)

    def test_init_with_invalid_datetime(self):
        data = {
            "id": "test_id",
            "created_at": "2022-01-01 00:00:00",
            "updated_at": "2022-01-02T00:00:00.000000",
        }
        with self.assertRaises(ValueError):
            BaseModel(**data)

    def test_save_updates_file_content(self):
        bm = BaseModel()
        bm.save()
        with open("file.json", "r") as f:
            file_content = f.read()
            self.assertIn(bm.id, file_content)
            self.assertIn(bm.to_dict()["created_at"], file_content)
            self.assertIn(bm.to_dict()["updated_at"], file_content)
            self.assertIn(bm.__class__.__name__, file_content)

    def test_updated_at_after_sleep(self):
        bm = BaseModel()
        u = bm.updated_at
        s = 0.1
        with patch('models.base_model.datetime') as mock_datetime:
            mock_datetime.now.return_value = u + timedelta(seconds=s)
            bm.save()
            self.assertNotEqual(u, bm.updated_at)

    def test_updated_at_not_updated_without_save(self):
        bm = BaseModel()
        i = bm.updated_at
        s = 0.1
        with patch('models.base_model.datetime') as mock_datetime:
            mock_datetime.now.return_value = i + timedelta(seconds=s)
            self.assertEqual(i, bm.updated_at)

    def test_save_with_args(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(None)

    def test_save_multiple_times(self):
        bm = BaseModel()
        initial_updated_at = bm.updated_at
        bm.save()
        self.assertNotEqual(initial_updated_at, bm.updated_at)
        second_updated_at = bm.updated_at
        bm.save()
        self.assertNotEqual(second_updated_at, bm.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        bm_str = bm.__str__()
        self.assertIn("[BaseModel] (123456)", bm_str)
        self.assertIn("'id': '123456'", bm_str)
        self.assertIn("'created_at': " + dt_repr, bm_str)
        self.assertIn("'updated_at': " + dt_repr, bm_str)

    def test_to_dict_with_arg(self):
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict(None)

    def test_to_dict_contains_added_attributes(self):
        bm = BaseModel()
        bm.name = "Holberton"
        bm.my_number = 98
        self.assertIn("name", bm.to_dict())
        self.assertIn("my_number", bm.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))


if __name__ == '__main__':
    unittest.main()
