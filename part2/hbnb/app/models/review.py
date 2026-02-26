#!/usr/bin/env python3
"""Review model module."""

from app.models import BaseModel


class Review(BaseModel):
    """Review class representing a review for a place in the system."""

    def __init__(self, text, rating, place, user):
        """Initialize a Review instance.

        Args:
            text (str): The content of the review. Required.
            rating (int): Rating given to the place. Must be between 1 and 5.
            place (Place): Place instance being reviewed.
            user (User): User instance who wrote the review.

        Raises:
            ValueError: If validation fails for any attribute.
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        """Get the review text."""
        return self._text

    @text.setter
    def text(self, value):
        """Set the review text with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Review text is required and must be a string")
        self._text = value

    @property
    def rating(self):
        """Get the rating."""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Set the rating with validation."""
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value

    @property
    def place(self):
        """Get the place."""
        return self._place

    @place.setter
    def place(self, value):
        """Set the place with validation."""
        from app.models.place import Place
        if not isinstance(value, Place):
            raise ValueError("Place must be a valid Place instance")
        self._place = value

    @property
    def user(self):
        """Get the user."""
        return self._user

    @user.setter
    def user(self, value):
        """Set the user with validation."""
        from app.models.user import User
        if not isinstance(value, User):
            raise ValueError("User must be a valid User instance")
        self._user = value