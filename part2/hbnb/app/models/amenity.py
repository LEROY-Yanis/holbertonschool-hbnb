#!/usr/bin/env python3
"""Amenity model module."""

from app.models import BaseModel


class Amenity(BaseModel):
    """Amenity class representing an amenity that can be associated with places."""

    def __init__(self, name, description=""):
        """Initialize an Amenity instance.

        Args:
            name (str): The name of the amenity. Required, max 50 chars.
            description (str): Description of the amenity. Optional.

        Raises:
            ValueError: If validation fails for the name attribute.
        """
        super().__init__()
        self.name = name
        self.description = description

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

    @property
    def description(self):
        """Get the description."""
        return self._description

    @description.setter
    def description(self, value):
        """Set the description."""
        if value is not None and not isinstance(value, str):
            raise ValueError("Description must be a string")
        self._description = value if value else ""