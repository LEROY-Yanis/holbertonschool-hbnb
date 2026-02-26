#!/usr/bin/env python3
"""Place model module."""

from app.models import BaseModel


class Place(BaseModel):
    """Place class representing a rental property in the system."""

    def __init__(self, title, description, price, latitude, longitude, owner):
        """Initialize a Place instance.

        Args:
            title (str): The title of the place. Required, max 100 chars.
            description (str): Detailed description of the place. Optional.
            price (float): The price per night. Must be positive.
            latitude (float): Latitude coordinate. Must be between -90.0 and 90.0.
            longitude (float): Longitude coordinate. Must be between -180.0 and 180.0.
            owner (User): User instance who owns the place.

        Raises:
            ValueError: If validation fails for any attribute.
        """
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    @property
    def title(self):
        """Get the title."""
        return self._title

    @title.setter
    def title(self, value):
        """Set the title with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Title is required and must be a string")
        if len(value) > 100:
            raise ValueError("Title must not exceed 100 characters")
        self._title = value

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

    @property
    def price(self):
        """Get the price."""
        return self._price

    @price.setter
    def price(self, value):
        """Set the price with validation."""
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number")
        if value <= 0:
            raise ValueError("Price must be a positive value")
        self._price = float(value)

    @property
    def latitude(self):
        """Get the latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Set the latitude with validation."""
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number")
        if value < -90.0 or value > 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self._latitude = float(value)

    @property
    def longitude(self):
        """Get the longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Set the longitude with validation."""
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number")
        if value < -180.0 or value > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        self._longitude = float(value)

    @property
    def owner(self):
        """Get the owner."""
        return self._owner

    @owner.setter
    def owner(self, value):
        """Set the owner with validation."""
        from app.models.user import User
        if not isinstance(value, User):
            raise ValueError("Owner must be a valid User instance")
        self._owner = value

    def add_review(self, review):
        """Add a review to the place.

        Args:
            review: Review instance to add.
        """
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place.

        Args:
            amenity: Amenity instance to add.
        """
        self.amenities.append(amenity)