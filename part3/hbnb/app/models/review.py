#!/usr/bin/env python3
"""Review model module."""

from app import db
from app.models import BaseModel


class Review(BaseModel):
    """Review class representing a review for a place in the system."""

    __tablename__ = 'reviews'

    _text = db.Column('text', db.Text, nullable=False)
    _rating = db.Column('rating', db.Integer, nullable=False)
    _place_id = db.Column('place_id', db.String(36), db.ForeignKey('places.id'), nullable=False)
    _user_id = db.Column('user_id', db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Add unique constraint: one review per user per place
    __table_args__ = (
        db.UniqueConstraint('user_id', 'place_id', name='unique_user_place_review'),
    )

    def __init__(self, text, rating, place=None, user=None, place_id=None, user_id=None, **kwargs):
        """Initialize a Review instance."""
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        if place:
            self._place_id = place.id
        elif place_id:
            self._place_id = place_id
        if user:
            self._user_id = user.id
        elif user_id:
            self._user_id = user_id

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
    def place_id(self):
        """Get the place's ID."""
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        """Set the place ID."""
        self._place_id = value

    @property
    def user_id(self):
        """Get the user's ID."""
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        """Set the user ID."""
        self._user_id = value