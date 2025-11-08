from app.models.basemodel import BaseModel

class Place(BaseModel):
	def __init__(self, title, description, price, latitude, longitude, owner_id, id=None, created_at=None, updated_at=None):
		super().__init__(id, created_at, updated_at)

		if not title or len(title.strip()) == 0:
			raise ValueError("title is required")
		if price is None or price <= 0:
			raise ValueError("price must be greater than 0") 
		if latitude is None or latitude < -90 or latitude > 90:
			raise ValueError("latitude must be between -90 and 90")
		if longitude is None or longitude < -180 or longitude > 180:
			raise ValueError("longitude must be between -180 and 180")
		if not owner_id:
			raise ValueError("owner_id is required")

		self.title = title
		self.description = description
		self.price = price
		self.latitude = latitude
		self.longitude = longitude
		self.owner_id = owner_id
		self.reviews = []  # List to store related reviews
		self.amenities = []  # List to store related amenity IDs

	def to_dict(self):
		return {
			'id': self.id,
			'title': self.title,
			'description': self.description,
			'price': self.price,
			'latitude': self.latitude,
			'longitude': self.longitude,
			'owner_id': self.owner_id,
			'created_at': self.created_at,
			'updated_at': self.updated_at
		}

	def update(self, data):
		for k, v in data.items():
			if k == 'title':
				if not v or len(v.strip()) == 0:
					raise ValueError("title is required")
				setattr(self, k, v)
			elif k == 'description':
				setattr(self, k, v)
			elif k == 'price':
				if v is None or v <= 0:
					raise ValueError("price must be greater than 0")
				setattr(self, k, v)
			elif k == 'latitude':
				if v is None or v < -90 or v > 90:
					raise ValueError("latitude must be between -90 and 90")
				setattr(self, k, v)
			elif k == 'longitude':
				if v is None or v < -180 or v > 180:
					raise ValueError("longitude must be between -180 and 180")
				setattr(self, k, v)
		self.save()
