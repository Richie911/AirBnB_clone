#!/usr/bin/python3
"""Defines the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represent a review.

    Attributes:
        user_id (str): The User id.
        place_id (str): The Place id.
        text (str): The text of the review.
    """
    user_id = ""
    place_id = ""
    text = ""