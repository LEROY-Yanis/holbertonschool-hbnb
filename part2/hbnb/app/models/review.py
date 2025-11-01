from app.models.basemodel import BaseModel

class Review(BaseModel):
	def __init__(self, text, rating, place_id, user_id, id=None, created_at=None, updated_at=None):
		super().__init__(id, created_at, updated_at)

		if not text or len(text.strip()) == 0:
			raise ValueError("text is required")
		if not place_id:
			raise ValueError("place_id is required")
		if not user_id:
			raise ValueError("user_id is required")
		if rating is None or not isinstance(rating, int) or rating < 1 or rating > 5:
			raise ValueError("rating must be an integer between 1 and 5")
		
		self.text = text
		self.rating = rating
		self.place_id = place_id
		self.user_id = user_id

	def to_dict(self):
		return {
			'id': self.id,
			'text': self.text,
			'rating': self.rating,
			'place_id': self.place_id,
			'user_id': self.user_id,
			'created_at': self.created_at,
			'updated_at': self.updated_at
		}

	def update(self, data):
		for k, v in data.items():
			if k == 'text':
				if not v or len(v.strip()) == 0:
					raise ValueError("text is required")
				setattr(self, k, v)
			elif k == 'rating':
				if v is None or not isinstance(v, int) or v < 1 or v > 5:
					raise ValueError("rating must be an integer between 1 and 5")
				setattr(self, k, v)
		self.save()
