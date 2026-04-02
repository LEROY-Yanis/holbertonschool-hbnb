#!/usr/bin/env python3
"""Place model module."""

from app import db
from app.models import BaseModel


# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Place(BaseModel):
    """Place class representing a rental property in the system."""

    __tablename__ = 'places'

    _title = db.Column('title', db.String(100), nullable=False)
    _description = db.Column('description', db.Text, default="")
    _price = db.Column('price', db.Float, nullable=False)
    _latitude = db.Column('latitude', db.Float, nullable=False)
    _longitude = db.Column('longitude', db.Float, nullable=False)
    _owner_id = db.Column('owner_id', db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                                 backref=db.backref('places', lazy=True))

    def __init__(self, title, description, price, latitude, longitude, owner=None, owner_id=None, **kwargs):
        """Initialize a Place instance."""
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        if owner:
            self._owner_id = owner.id
        elif owner_id:
            self._owner_id = owner_id

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
    def owner_id(self):
        """Get the owner's ID."""
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        """Set the owner ID."""
        self._owner_id = value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)