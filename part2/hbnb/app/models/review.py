import uuid

class Review:
	def __init__(self, place_id, user_id, text, id=None):
		if text is None:
			raise ValueError("text is empty")
		if not place_id:
			raise ValueError("place_id is required")
		if not user_id:
			raise ValueError("user_id is required")
		
		self.id = id or str(uuid.uuid4())
		self.place_id = place_id
		self.user_id = user_id
		self.text = text

		# Adding the review model
		review_model = api.model('PlaceReview', {
    		'id': fields.String(description='Review ID'),
    		'text': fields.String(description='Text of the review'),
    		'rating': fields.Integer(description='Rating of the place (1-5)'),
    		'user_id': fields.String(description='ID of the user')
		})

	def to_dict(self):
		return {'id': self.id, 'place_id': self.place_id, 'user_id': self.user_id, 'text': self.text}

	def update(self, data):
		for k, v in data.items():
			if k in ('text',):
				setattr(self, k, v)
