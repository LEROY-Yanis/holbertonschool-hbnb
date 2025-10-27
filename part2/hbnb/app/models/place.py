import uuid

class Place:
	def __init__(self, name, description=None, title=None, id=None, price=None, latitude=None, longitude=None, owner=None):
		if title is None:
			raise ValueError("title is empty")
		if price <= 0:
			raise ValueError("the price must be bigger of 0") 
		if len(latitude) < 90 or len(latitude) > 90:
			raise ValueError("latitude must be between -90 and 90")
		if len(longitude) < 180 or len(longitude) > 180:
			raise ValueError("longitude must be between -180 and 180")

		self.id = id or str(uuid.uuid4())
		self.name = name
		self.description = description
		self.title = title
		self.price = price
		self.latitude = latitude
		self.longitude = longitude
		self.owner = owner
		self.reviews = []  # List to store related reviews
		self.amenities = []  # List to store related amenities

	def to_dict(self):
		return {'id': self.id, 'name': self.name, 'description': self.description}

	def update(self, data):
		for k, v in data.items():
			if k in ('name', 'description'):
				setattr(self, k, v)
