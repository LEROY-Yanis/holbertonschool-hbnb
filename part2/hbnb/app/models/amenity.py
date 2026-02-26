#!/usr/bin/env python3
"""Amenity model module."""

from app.models import BaseModel


class Amenity(BaseModel):
    """Amenity class representing an amenity that can be associated with places."""

    def __init__(self, name):
        """Initialize an Amenity instance.

        Args:
            name (str): The name of the amenity. Required, max 50 chars.

        Raises:
            ValueError: If validation fails for the name attribute.
        """
        super().__init__()
        self.name = name

    @property
    def name(self):
        """Get the name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the name with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Amenity name is required and must be a string")
        if len(value) > 50:
            raise ValueError("Amenity name must not exceed 50 characters")
        self._name = value