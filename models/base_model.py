#!/usr/bin/python3
"""
Base Model Module
"""

from datetime import date, datetime
from uuid import uuid4
import models


class BaseModel:
    """
    Base class for all other models in the project.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Attributes:
            id (str): Unique identifier for the instance
            created_at (datetime): Date and time of instance creation
            updated_at (datetime): Date and time of instance update

        If `kwargs` is not empty, it creates an instance from a dictionary representation
        Otherwise, it creates a new instance with a new id and sets created_at and updated_at
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                elif key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """
        Return the string representation of the BaseModel

        Returns:
            str: String representation in the format: "[<class name>] (<id>) <__dict__>"
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Update the public instance attribute 'updated_at' with the current datetime and save to storage
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Return a dictionary containing all keys/values of the instance

        Returns:
            dict: Dictionary representation of the instance with ISO-formatted dates
        """
        new_dict = self.__dict__.copy()
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        new_dict["__class__"] = self.__class__.__name__
        return new_dict
