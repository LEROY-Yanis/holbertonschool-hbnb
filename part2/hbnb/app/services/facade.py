from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User methods
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if user:
            user.update(user_data)
        return user

    # Amenity methods
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if amenity:
            amenity.update(amenity_data)
        return amenity

    # Place methods
    def create_place(self, place_data):
        # Validate owner exists
        owner = self.get_user(place_data.get('owner_id'))
        if not owner:
            return None
        
        # Validate amenities exist
        amenity_ids = place_data.get('amenities', [])
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                return None
        
        # Create place
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner_id=place_data.get('owner_id')
        )
        place.amenities = amenity_ids
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None
        
        # Validate amenities if provided
        if 'amenities' in place_data:
            amenity_ids = place_data.get('amenities', [])
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    return None
            place.amenities = amenity_ids
            del place_data['amenities']
        
        place.update(place_data)
        return place

    # Review methods
    def create_review(self, review_data):
        # Validate user exists
        user = self.get_user(review_data.get('user_id'))
        if not user:
            return None
        
        # Validate place exists
        place = self.get_place(review_data.get('place_id'))
        if not place:
            return None
        
        # Create review
        review = Review(**review_data)
        self.review_repo.add(review)
        
        # Add review to place
        if review.id not in place.reviews:
            place.reviews.append(review.id)
        
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if review:
            review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False
        
        # Remove review from place
        place = self.get_place(review.place_id)
        if place and review.id in place.reviews:
            place.reviews.remove(review.id)
        
        self.review_repo.delete(review_id)
        return True
