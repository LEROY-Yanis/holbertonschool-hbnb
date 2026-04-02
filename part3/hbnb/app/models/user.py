#!/usr/bin/env python3
"""User model module."""

import re
from app import db, bcrypt
from app.models import BaseModel


class User(BaseModel):
    """User class representing a user in the system."""

    __tablename__ = 'users'

    _first_name = db.Column('first_name', db.String(50), nullable=False)
    _last_name = db.Column('last_name', db.String(50), nullable=False)
    _email = db.Column('email', db.String(120), nullable=False, unique=True)
    _password = db.Column('password', db.String(128), nullable=False)
    _is_admin = db.Column('is_admin', db.Boolean, default=False)

    # Relationships will be added later
    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False, **kwargs):
        """Initialize a User instance."""
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    @property
    def first_name(self):
        """Get the first name."""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """Set the first name with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("First name is required and must be a string")
        if len(value) > 50:
            raise ValueError("First name must not exceed 50 characters")
        self._first_name = value

    @property
    def last_name(self):
        """Get the last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """Set the last name with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Last name is required and must be a string")
        if len(value) > 50:
            raise ValueError("Last name must not exceed 50 characters")
        self._last_name = value

    @property
    def email(self):
        """Get the email."""
        return self._email

    @email.setter
    def email(self, value):
        """Set the email with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Email is required and must be a string")
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise ValueError("Invalid email format")
        self._email = value

    @property
    def is_admin(self):
        """Get the admin status."""
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        """Set the admin status with validation."""
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean")
        self._is_admin = value

    @property
    def password(self):
        """Get the stored password hash."""
        return self._password

    @password.setter
    def password(self, value):
        """Set the password as a bcrypt hash."""
        if not value or not isinstance(value, str):
            raise ValueError("Password is required and must be a string")

        # Keep already-hashed bcrypt strings untouched.
        if value.startswith('$2a$') or value.startswith('$2b$') or value.startswith('$2y$'):
            self._password = value
            return

        self._password = bcrypt.generate_password_hash(value).decode('utf-8')

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = password

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def create_user(first_name, last_name, email, password=None, is_admin=False):
        """Factory method to create a new user."""
        return User(first_name, last_name, email, password, is_admin)