import uuid

class User:
	def __init__(self, email, name=None, id=None):
		self.id = id or str(uuid.uuid4())
		self.email = email
		self.name = name

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
