#!/usr/bin/python3
from datetime import datetime
import uuid
from models import storage

class BaseModel:
    """base class"""

    def __init__(self,*args, **kwargs):
        """
        initializes the base model
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if len(kwargs) > 0:
            for key,value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = value
        else:
            storage.new(self)

    def save(self):
        """updates the public instance attribute updated_at with the current datetime"""

        self.updated_at = datetime.now()
        storage.save()

    def __str__(self):
        """print: [<class name>] (<self.id>) <self.__dict__>"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
    
    def to_dict(self):
        """returns a dictionary containing all keys/values of __dict__ of the instance"""
        variable = self.__dict__
        variable["updated_at"] = variable["updated_at"].isoformat()
        variable["created_at"] = variable["created_at"].isoformat()
        variable["__class__"] = self.__class__.__name__
        return variable