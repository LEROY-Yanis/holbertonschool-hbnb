import re
from app.models.basemodel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False, id=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)

        if len(first_name) == 0 or len(first_name) > 50:
            raise ValueError("first name must be between 1 and 50 characters")
        if len(last_name) == 0 or len(last_name) > 50:
            raise ValueError("last name must be between 1 and 50 characters")
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean")
        if not email:
            raise ValueError("email is required")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("invalid email format")

        # Specific attributes for User
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.validate()

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update(self, data):
        for k, v in data.items():
            if k in ('email', 'name'):
                setattr(self, k, v)
