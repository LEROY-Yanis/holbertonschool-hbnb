#!/usr/bin/env python3
"""Facade module for HBnB application."""

from app.persistence.repository import UserRepository, PlaceRepository, ReviewRepository, AmenityRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """Facade class to manage all business logic operations."""

    def __init__(self):
        """Initialize repositories for all entities."""
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # ==================== User Methods ====================

    def create_user(self, user_data):
        """Create a new user."""
        payload = dict(user_data)
        password = payload.pop('password', None)
        if not password:
            raise ValueError("password is required")

        user = User(password=password, **payload)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get a user by email."""
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Get all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information."""
        from app import db

        user = self.user_repo.get(user_id)
        if not user:
            return None

        payload = dict(user_data)
        password = payload.pop('password', None)

        for key, value in payload.items():
            setattr(user, key, value)

        if password is not None:
            user.password = password

        db.session.commit()
        return user

    # ==================== Amenity Methods ====================

    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity's information."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    # ==================== Place Methods ====================

    def create_place(self, place_data):
        """Create a new place."""
        # Get the owner from owner_id
        owner_id = place_data.pop('owner_id', None)
        if not owner_id:
            raise ValueError("owner_id is required")

        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        # Handle amenities
        amenity_ids = place_data.pop('amenities', [])

        # Create place with owner_id
        place = Place(owner_id=owner_id, **place_data)

        # Add amenities to place
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if amenity:
                place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place's information."""
        from app import db
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Handle amenities update if provided
        if 'amenities' in place_data:
            amenity_ids = place_data.pop('amenities')
            place.amenities = []
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    # ==================== Review Methods ====================

    def create_review(self, review_data):
        """Create a new review."""
        # Get user and place from IDs
        user_id = review_data.pop('user_id', None)
        place_id = review_data.pop('place_id', None)

        if not user_id:
            raise ValueError("user_id is required")
        if not place_id:
            raise ValueError("place_id is required")

        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        # Create review with IDs
        review = Review(user_id=user_id, place_id=place_id, **review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place."""
        place = self.get_place(place_id)
        if not place:
            return None
        return self.review_repo.get_reviews_by_place(place_id)

    def user_has_reviewed_place(self, user_id, place_id):
        """Check whether a user has already reviewed a place."""
        return self.review_repo.get_user_review_for_place(user_id, place_id) is not None

    def update_review(self, review_id, review_data):
        """Update a review's information."""
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        """Delete a review."""
        review = self.review_repo.get(review_id)
        if not review:
            return False
        return self.review_repo.delete(review_id)