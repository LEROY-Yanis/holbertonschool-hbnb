from app.models.basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, id=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)

        if not name or len(name.strip()) == 0:
            raise ValueError("name is required")
        if len(name) > 50:
            raise ValueError("name must not exceed 50 characters")

        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def update(self, data):
        for k, v in data.items():
            if k == 'name':
                if not v or len(v.strip()) == 0:
                    raise ValueError("name is required")
                if len(v) > 50:
                    raise ValueError("name must not exceed 50 characters")
                setattr(self, k, v)
        self.save()
