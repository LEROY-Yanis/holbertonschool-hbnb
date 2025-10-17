import uuid

class Place:
	def __init__(self, name, description=None, id=None):
		self.id = id or str(uuid.uuid4())
		self.name = name
		self.description = description

	def to_dict(self):
		return {'id': self.id, 'name': self.name, 'description': self.description}

	def update(self, data):
		for k, v in data.items():
			if k in ('name', 'description'):
				setattr(self, k, v)
