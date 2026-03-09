#!/usr/bin/env python3
"""User model module."""

import re
from app.models import BaseModel


class User(BaseModel):
    """User class representing a user in the system."""

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        """Initialize a User instance.

        Args:
            first_name (str): The first name of the user. Required, max 50 chars.
            last_name (str): The last name of the user. Required, max 50 chars.
            email (str): The email address of the user. Required, must be valid format.
            password (str): The password of the user. Optional for now.
            is_admin (bool): Whether the user has admin privileges. Defaults to False.

        Raises:
            ValueError: If validation fails for any attribute.
        """
        super().__init__()
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
        # Simple email validation regex
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
        """Get the password."""
        return self._password

    @password.setter
    def password(self, value):
        """Set the password."""
        # Password will be hashed in Part 3
        self._password = value

    @staticmethod
    def create_user(first_name, last_name, email, password=None, is_admin=False):
        """Factory method to create a new user.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            email (str): The email address of the user.
            password (str): The password of the user.
            is_admin (bool): Whether the user has admin privileges.

        Returns:
            User: A new User instance.
        """
        return User(first_name, last_name, email, password, is_admin)