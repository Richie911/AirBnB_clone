#!/usr/bin/python3
import os
import json

class FileStorage:
    """ storage class"""
    def __init__(self):
        self.__file_path = 'file.json'
        self.__objects = {}

    def all(self): 
        return self.__dict__
    
    def new(self, obj):
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj.id

    def save(self): 
        json_string = json.dumps(self.__objects)
        with open(self.__file_path, 'a') as file:
            file.write(json_string)
    
    def reload(self):
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r') as file:
                content = file.read()
                my_dict = json.loads(content)
                self.__objects = my_dict
