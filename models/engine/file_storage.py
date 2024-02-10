#!/usr/bin/python3
from datetime import datetime
import os
import json

import models

class FileStorage:
    """ storage class"""
    def __init__(self):
        self.__file_path = 'file.json'
        self.__objects = {}

    def all(self): 
        return self.__objects
    
    def new(self, obj):
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj.__dict__

    def save(self):
        """Serialize __objects to the JSON file."""
        with open(self.__file_path, "w") as file:
            json.dump(self.__objects, file, default=self.json_serializable)

    def json_serializable(self, obj):
        """Handle serialization of non-serializable objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    def reload(self):
        """Deserialize the JSON file to objects."""
        try:
            with open(self.__file_path, 'r') as f:
                data = json.load(f)
                for key, value in data.items():
                    if '__class__' in value:
                        class_name = value['__class__']
                        model_class = getattr(__import__('models', fromlist=[class_name]), class_name)
                        obj = model_class(**value)
                self.__objects = data
                return data
        except FileNotFoundError:
            pass


