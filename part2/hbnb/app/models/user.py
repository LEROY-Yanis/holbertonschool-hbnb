#!/usr/bin/env python3
"""User model module."""

import re
from app.models import BaseModel


class User(BaseModel):
    """User class representing a user in the system."""

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialize a User instance.

        Args:
            first_name (str): The first name of the user. Required, max 50 chars.
            last_name (str): The last name of the user. Required, max 50 chars.
            email (str): The email address of the user. Required, must be valid format.
            is_admin (bool): Whether the user has admin privileges. Defaults to False.

        Raises:
            ValueError: If validation fails for any attribute.
        """
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
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

import re
from app.models import BaseModel


class User(BaseModel):
    """User model representing application users."""

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self._validate()

    def _validate(self):
        """Validate user data."""
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError("First name is required and must be at most 50 characters")
        if not self.last_name or len(self.last_name) > 50:
            raise ValueError("Last name is required and must be at most 50 characters")
        if not self.email or not self._is_valid_email(self.email):
            raise ValueError("Valid email is required")

    @staticmethod
    def _is_valid_email(email):
        """Check if email format is valid."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None