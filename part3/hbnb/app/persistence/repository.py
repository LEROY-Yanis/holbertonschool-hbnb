#!/usr/bin/env python3

from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)


class SQLAlchemyRepository(Repository):
    """SQLAlchemy-based repository for database persistence."""

    def __init__(self, model):
        """Initialize with a SQLAlchemy model class."""
        self.model = model

    def add(self, obj):
        """Add an object to the database."""
        from app import db
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Get an object by its ID."""
        from app import db
        return db.session.get(self.model, obj_id)

    def get_all(self):
        """Get all objects of this model."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object with the given data."""
        from app import db
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
        return obj

    def delete(self, obj_id):
        """Delete an object by its ID."""
        from app import db
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by a specific attribute."""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()


class UserRepository(SQLAlchemyRepository):
    """Repository for User entity with user-specific queries."""

    def __init__(self):
        from app.models.user import User
        super().__init__(User)

    def get_user_by_email(self, email):
        """Get a user by their email address."""
        return self.model.query.filter_by(_email=email).first()


class PlaceRepository(SQLAlchemyRepository):
    """Repository for Place entity with place-specific queries."""

    def __init__(self):
        from app.models.place import Place
        super().__init__(Place)

    def get_places_by_owner(self, owner_id):
        """Get all places owned by a specific user."""
        return self.model.query.filter_by(_owner_id=owner_id).all()


class ReviewRepository(SQLAlchemyRepository):
    """Repository for Review entity with review-specific queries."""

    def __init__(self):
        from app.models.review import Review
        super().__init__(Review)

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place."""
        return self.model.query.filter_by(_place_id=place_id).all()

    def get_reviews_by_user(self, user_id):
        """Get all reviews written by a specific user."""
        return self.model.query.filter_by(_user_id=user_id).all()

    def get_user_review_for_place(self, user_id, place_id):
        """Check if a user has already reviewed a place."""
        return self.model.query.filter_by(_user_id=user_id, _place_id=place_id).first()


class AmenityRepository(SQLAlchemyRepository):
    """Repository for Amenity entity with amenity-specific queries."""

    def __init__(self):
        from app.models.amenity import Amenity
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        """Get an amenity by its name."""
        return self.model.query.filter_by(_name=name).first()
